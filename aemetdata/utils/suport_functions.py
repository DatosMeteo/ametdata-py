from __future__ import annotations

import asyncio
import io
import logging
import os
import time
import tarfile
from typing import Iterable

import httpx


logger = logging.getLogger(__name__)

MAX_CICLOS = 5  # more retries to survive transient disconnects
# AEMET allows ~150 requests per 5-minute window (30 req/min).
# Enforcing a 2.5 s minimum interval keeps us safely under the limit.
# Set env var AEMET_REQUEST_INTERVAL=0 to disable (e.g. in tests).
_last_request_time: float = 0.0


class AemetError(Exception):
    """Excepcion personalizada para errores de AEMET."""
    pass


async def _rate_limit() -> None:
    """Enforces a minimum interval between AEMET API requests."""
    global _last_request_time
    interval = float(os.environ.get("AEMET_REQUEST_INTERVAL", "2.5"))
    if interval <= 0:
        return
    elapsed = time.monotonic() - _last_request_time
    if elapsed < interval:
        await asyncio.sleep(interval - elapsed)
    _last_request_time = time.monotonic()



def get_relativedelta():
    try:
        from dateutil.relativedelta import relativedelta
        return relativedelta
    except ImportError:
        raise ImportError(
            "Falta el paquete 'python-dateutil'. Instalalo con 'pip install python-dateutil'."
        )


def validar_api_keys(api_keys: Iterable[str]) -> list[str]:
    """Valida y convierte api_keys a lista no vacia.

    Args:
        api_keys: Iterable de claves API.

    Returns:
        Lista de claves API.

    Raises:
        ValueError: Si la lista esta vacia.
    """
    keys = list(api_keys)
    if not keys:
        raise ValueError("Se requiere al menos una API key en 'api_keys'.")
    return keys


def procesar_lista_ids(valor, nombre_param: str = "idema") -> list[str]:
    """Convierte un str o iterable de str en lista.

    Args:
        valor: str o iterable de str.
        nombre_param: Nombre del parametro para mensajes de error.

    Returns:
        Lista de identificadores.

    Raises:
        ValueError: Si el tipo no es valido o la lista esta vacia.
    """
    if isinstance(valor, str):
        resultado = [valor]
    elif isinstance(valor, (list, tuple)):
        resultado = list(valor)
    else:
        raise ValueError(f"El parametro '{nombre_param}' debe ser str o iterable de str.")
    if not resultado:
        raise ValueError(f"El parametro '{nombre_param}' es obligatorio.")
    return resultado


def normalizar_datos(datos) -> list:
    """Normaliza el resultado de AEMET a lista.

    Args:
        datos: Respuesta de la URL de datos de AEMET (dict, list o str JSON).

    Returns:
        Lista de registros.
    """
    import json as _json

    if isinstance(datos, list):
        return datos
    if isinstance(datos, dict):
        return [datos]
    try:
        parsed = _json.loads(datos)
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict):
            return [parsed]
        return [{"contenido": str(datos)}]
    except Exception:
        return [{"contenido": str(datos)}]


async def fetch_json_url(url: str, descripcion: str | None = None):
    """Descarga un JSON desde una URL y lo devuelve como dict/list.

    Args:
        url: URL del recurso JSON.
        descripcion: Texto opcional para contextualizar errores.

    Raises:
        AemetError: Si la descarga falla o el contenido no es JSON.
    """
    import json as _json

    contexto = f" ({descripcion})" if descripcion else ""
    logger.debug("Descargando JSON%s desde: %s", contexto, url)

    async def _via_httpx():
        _LIMITS = httpx.Limits(max_keepalive_connections=0, max_connections=5)
        async with httpx.AsyncClient(limits=_LIMITS) as client:
            resp = await client.get(url, timeout=30)
            resp.raise_for_status()
        try:
            return resp.json()
        except Exception:
            try:
                return _json.loads(resp.content.decode("utf-8"))
            except (UnicodeDecodeError, ValueError):
                return _json.loads(resp.content.decode("latin-1"))

    async def _via_urllib():
        import urllib.request as _urllib
        def _download() -> bytes:
            req = _urllib.Request(url, headers={"User-Agent": "aemetdata-py/0.1"})
            with _urllib.urlopen(req, timeout=30) as r:
                return r.read()
        content = await asyncio.to_thread(_download)
        try:
            return _json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            return _json.loads(content.decode("latin-1"))

    last_exc: Exception | None = None

    for attempt in range(3):
        try:
            return await _via_httpx()
        except (httpx.RemoteProtocolError, httpx.ConnectError, httpx.ReadError) as exc:
            logger.warning(
                "httpx disconnect intento %d para JSON%s, reintentando con urllib: %s",
                attempt + 1, contexto, exc,
            )
            try:
                return await _via_urllib()
            except Exception as exc2:
                last_exc = exc2
                logger.warning("urllib también falló intento %d%s: %s", attempt + 1, contexto, exc2)
                if attempt < 2:
                    await asyncio.sleep(1 + attempt)
        except (ValueError, _json.JSONDecodeError) as exc:
            # Empty or non-JSON response body from a successful HTTP request
            last_exc = exc
            raise AemetError(f"Respuesta no es JSON válido{contexto}: {exc}") from exc
        except httpx.HTTPError as exc:
            last_exc = exc
            if attempt < 2:
                await asyncio.sleep(1 + attempt)
            else:
                raise AemetError(f"Error descargando JSON{contexto}: {exc}") from exc

    raise AemetError(f"Error descargando JSON{contexto}: {last_exc}") from last_exc


async def fetch_bytes_url(url: str, descripcion: str | None = None) -> bytes:
    """Descarga contenido binario desde una URL.

    Args:
        url: URL del recurso.
        descripcion: Texto opcional para contextualizar errores.

    Returns:
        Contenido binario de la respuesta.

    Raises:
        AemetError: Si la descarga falla.
    """
    import urllib.request as _urllib

    contexto = f" ({descripcion})" if descripcion else ""
    logger.debug("Descargando contenido binario%s desde: %s", contexto, url)

    async def _via_httpx() -> bytes:
        _LIMITS = httpx.Limits(max_keepalive_connections=0, max_connections=5)
        async with httpx.AsyncClient(limits=_LIMITS) as client:
            resp = await client.get(url, timeout=60)
            resp.raise_for_status()
            return resp.content

    async def _via_urllib() -> bytes:
        def _download() -> bytes:
            req = _urllib.Request(url, headers={"User-Agent": "aemetdata-py/0.1"})
            with _urllib.urlopen(req, timeout=60) as r:
                return r.read()
        return await asyncio.to_thread(_download)

    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            return await _via_httpx()
        except (httpx.RemoteProtocolError, httpx.ConnectError, httpx.ReadError) as exc:
            logger.warning(
                "httpx disconnect intento %d para binario%s, reintentando con urllib: %s",
                attempt + 1, contexto, exc,
            )
            try:
                return await _via_urllib()
            except Exception as exc2:
                last_exc = exc2
                if attempt < 2:
                    await asyncio.sleep(1 + attempt)
        except httpx.HTTPError as exc:
            last_exc = exc
            if attempt < 2:
                await asyncio.sleep(1 + attempt)
            else:
                raise AemetError(f"Error descargando contenido{contexto}: {exc}") from exc

    raise AemetError(f"Error descargando contenido{contexto}: {last_exc}") from last_exc


async def fetch_con_reintentos_endpoint_aemet(
    url_template: str,
    tipo: str,
    api_keys: list[str],
) -> dict:
    """Realiza una peticion a AEMET con rotacion de claves API y reintentos.

    La logica aplica hasta MAX_CICLOS vueltas sobre todas las api_keys.
    En cada intento espera un backoff exponencial antes de probar la siguiente clave.

    Args:
        url_template: URL con {apiKey} como marcador de posicion para la clave.
        tipo: Identificador de la operacion para logs.
        api_keys: Lista de claves API de AEMET.

    Returns:
        Respuesta JSON como diccionario.

    Raises:
        AemetError: Si ninguna clave funciona tras MAX_CICLOS ciclos.
    """
    logger.info("Iniciando peticion a AEMET [%s]", tipo)
    ciclos_completados = 0

    while ciclos_completados < MAX_CICLOS:
        logger.debug("Ciclo %d de %d [%s]", ciclos_completados + 1, MAX_CICLOS, tipo)

        for key_index, api_key in enumerate(api_keys):
            endpoint = url_template.replace("{apiKey}", api_key)
            logger.debug("Probando clave %d para [%s]", key_index + 1, tipo)

            async def _endpoint_via_httpx(url: str) -> dict:
                import json as _json
                _LIMITS = httpx.Limits(max_keepalive_connections=0, max_connections=5)
                async with httpx.AsyncClient(limits=_LIMITS) as client:
                    resp = await client.get(url, timeout=15)
                    resp.raise_for_status()
                content_type = resp.headers.get("Content-Type", "")
                if "application/json" not in content_type:
                    raise AemetError(f"Respuesta no JSON: {content_type!r}")
                try:
                    return resp.json()
                except Exception:
                    try:
                        return _json.loads(resp.content.decode("utf-8"))
                    except (UnicodeDecodeError, ValueError):
                        return _json.loads(resp.content.decode("latin-1"))

            async def _endpoint_via_urllib(url: str) -> dict:
                import json as _json, urllib.request as _urllib
                def _fetch() -> bytes:
                    req = _urllib.Request(url, headers={"User-Agent": "aemetdata-py/0.1"})
                    with _urllib.urlopen(req, timeout=15) as r:
                        return r.read()
                content = await asyncio.to_thread(_fetch)
                try:
                    data = _json.loads(content.decode("utf-8"))
                except (UnicodeDecodeError, ValueError):
                    data = _json.loads(content.decode("latin-1"))
                if not isinstance(data, dict):
                    raise AemetError(f"Respuesta inesperada (no dict): {type(data)}")
                return data

            try:
                await _rate_limit()
                try:
                    data = await _endpoint_via_httpx(endpoint)
                except (httpx.RemoteProtocolError, httpx.ConnectError, httpx.ReadError) as exc:
                    logger.warning(
                        "httpx disconnect clave %d [%s], reintentando con urllib: %s",
                        key_index + 1, tipo, exc,
                    )
                    data = await _endpoint_via_urllib(endpoint)

                logger.info("Datos obtenidos con clave %d [%s]", key_index + 1, tipo)
                return data

            except httpx.HTTPStatusError as exc:
                logger.warning(
                    "HTTP %d con clave %d [%s]",
                    exc.response.status_code, key_index + 1, tipo,
                )
            except Exception as exc:
                logger.warning(
                    "Error con clave %d [%s]: %s",
                    key_index + 1, tipo, exc,
                )

            espera = min(5 * (2 ** key_index), 60)
            logger.debug(
                "Esperando %ds antes de probar siguiente clave [%s]", espera, tipo
            )
            await asyncio.sleep(espera)

        ciclos_completados += 1
        logger.info("Fin de ciclo %d [%s]", ciclos_completados, tipo)

    raise AemetError(
        f"No se pudo realizar la solicitud '{tipo}' tras {MAX_CICLOS} ciclos."
    )


async def fetch_aemet_datos(
    endpoint_template: str,
    tipo: str,
    api_keys: list[str],
    descripcion: str | None = None,
) -> list:
    """Patron completo de descarga AEMET: primera llamada + segunda llamada a datos.

    Obtiene la URL de datos de la primera respuesta de AEMET y descarga el JSON
    de esa URL, devolviendo los registros normalizados como lista.

    Args:
        endpoint_template: URL con {apiKey} como marcador.
        tipo: Identificador para logs.
        api_keys: Lista de claves API.
        descripcion: Texto opcional para logs de la segunda descarga.

    Returns:
        Lista de registros.

    Raises:
        AemetError: Si hay error en cualquier paso.
    """
    response = await fetch_con_reintentos_endpoint_aemet(endpoint_template, tipo, api_keys)

    if response.get("estado") != 200:
        raise AemetError(
            f"Error en AEMET [{tipo}]: {response.get('descripcion', 'Error desconocido')} "
            f"(estado: {response.get('estado')})"
        )

    datos_url = response.get("datos")
    if not datos_url:
        raise AemetError(f"No se encontro URL de descarga en la respuesta de AEMET [{tipo}]")

    logger.info("Descargando datos desde URL de AEMET [%s]", tipo)
    datos = await fetch_json_url(datos_url, descripcion or tipo)
    logger.info("Datos descargados correctamente [%s]", tipo)

    return normalizar_datos(datos)


async def descargar_archivo_tar_gz(url: str) -> dict:
    """Descarga un archivo desde una URL y extrae su contenido.

    Soporta formatos: tar.gz, tar.bz2, zip y archivos simples.

    Args:
        url: URL del archivo.

    Returns:
        Diccionario con los archivos extraidos {nombre_archivo: contenido}.

    Raises:
        AemetError: Si hay error descargando o extrayendo el archivo.
    """
    import zipfile

    logger.debug("Descargando archivo desde: %s", url)

    import urllib.request as _urllib

    async def _descarga_via_httpx() -> bytes:
        _LIMITS = httpx.Limits(max_keepalive_connections=0, max_connections=5)
        async with httpx.AsyncClient(limits=_LIMITS) as client:
            resp = await client.get(url, timeout=60)
            resp.raise_for_status()
            return resp.content

    async def _descarga_via_urllib() -> bytes:
        def _download() -> bytes:
            req = _urllib.Request(url, headers={"User-Agent": "aemetdata-py/0.1"})
            with _urllib.urlopen(req, timeout=60) as r:
                return r.read()
        return await asyncio.to_thread(_download)

    try:
        try:
            content = await _descarga_via_httpx()
        except (httpx.RemoteProtocolError, httpx.ConnectError, httpx.ReadError) as exc:
            logger.warning("httpx disconnect para archivo, reintentando con urllib: %s", exc)
            content = await _descarga_via_urllib()
        magic_bytes = content[:4]
        files_content: dict[str, str] = {}

        def _leer_miembro(data: bytes) -> str:
            try:
                return data.decode("utf-8")
            except UnicodeDecodeError:
                return data.hex()

        # tar.gz
        if magic_bytes[:2] == b"\x1f\x8b":
            logger.debug("Formato detectado: tar.gz")
            try:
                tar_bytes = io.BytesIO(content)
                with tarfile.open(fileobj=tar_bytes, mode="r:gz") as tar:
                    for member in tar.getmembers():
                        if member.isfile():
                            f = tar.extractfile(member)
                            if f:
                                files_content[member.name] = _leer_miembro(f.read())
                                logger.debug("Extraido: %s", member.name)
                return files_content
            except Exception as exc:
                logger.warning("Fallo con tar.gz: %s", exc)

        # tar.bz2
        elif magic_bytes[:3] == b"BZh":
            logger.debug("Formato detectado: tar.bz2")
            try:
                tar_bytes = io.BytesIO(content)
                with tarfile.open(fileobj=tar_bytes, mode="r:bz2") as tar:
                    for member in tar.getmembers():
                        if member.isfile():
                            f = tar.extractfile(member)
                            if f:
                                files_content[member.name] = _leer_miembro(f.read())
                                logger.debug("Extraido: %s", member.name)
                return files_content
            except Exception as exc:
                logger.warning("Fallo con tar.bz2: %s", exc)

        # ZIP
        elif magic_bytes[:2] == b"PK":
            logger.debug("Formato detectado: ZIP")
            try:
                zip_bytes = io.BytesIO(content)
                with zipfile.ZipFile(zip_bytes, "r") as zip_ref:
                    for info in zip_ref.infolist():
                        if not info.is_dir():
                            files_content[info.filename] = _leer_miembro(
                                zip_ref.read(info)
                            )
                            logger.debug("Extraido: %s", info.filename)
                return files_content
            except Exception as exc:
                logger.warning("Fallo con ZIP: %s", exc)

        # tar simple
        elif magic_bytes[:6] == b"ustar\x00" or content[:256].find(b"ustar") != -1:
            logger.debug("Formato detectado: tar")
            try:
                tar_bytes = io.BytesIO(content)
                with tarfile.open(fileobj=tar_bytes, mode="r") as tar:
                    for member in tar.getmembers():
                        if member.isfile():
                            f = tar.extractfile(member)
                            if f:
                                files_content[member.name] = _leer_miembro(f.read())
                                logger.debug("Extraido: %s", member.name)
                return files_content
            except Exception as exc:
                logger.warning("Fallo con tar: %s", exc)

        # Contenido directo
        logger.debug("Formato desconocido, se devuelve como contenido directo")
        filename = url.split("/")[-1] or "descargado"
        files_content[filename] = _leer_miembro(content)
        return files_content

    except httpx.HTTPError as http_error:
        raise AemetError(f"Error descargando archivo: {http_error}") from http_error
    except Exception as exc:
        raise AemetError(f"Error descargando archivo: {exc}") from exc

