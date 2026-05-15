"""Modulo de avisos de AEMET.

Incluye avisos CAP (Common Alerting Protocol) y avisos vectoriales georreferenciados.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta
from typing import Iterable

from ..utils.suport_functions import (
    AemetError,
    descargar_archivo_tar_gz,
    fetch_con_reintentos_endpoint_aemet,
    validar_api_keys,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://opendata.aemet.es/opendata"

AREA_CODES: dict[str, str] = {
    "esp": "Espana",
    "61": "Andalucia",
    "62": "Aragon",
    "63": "Asturias, Principado de",
    "64": "Ballears, Illes",
    "78": "Ceuta",
    "65": "Canarias",
    "66": "Cantabria",
    "67": "Castilla y Leon",
    "68": "Castilla - La Mancha",
    "69": "Cataluna",
    "77": "Comunitat Valenciana",
    "70": "Extremadura",
    "71": "Galicia",
    "72": "Madrid, Comunidad de",
    "79": "Melilla",
    "73": "Murcia, Region de",
    "74": "Navarra, Comunidad Foral de",
    "75": "Pais Vasco",
    "76": "Rioja, La",
}

_FORMATO_COMPLETA = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}UTC$")
_FORMATO_SIMPLE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _completar_fecha(fecha: str, inicio: bool) -> str:
    if _FORMATO_COMPLETA.match(fecha):
        return fecha
    if _FORMATO_SIMPLE.match(fecha):
        return f"{fecha}T00:00:00UTC" if inicio else f"{fecha}T23:59:59UTC"
    raise ValueError(
        f"La fecha '{fecha}' debe estar en formato 'AAAA-MM-DD' o 'AAAA-MM-DDTHH:MM:SSUTC'."
    )


def _parse_fecha(fecha: str) -> datetime:
    if "T" in fecha:
        return datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%SUTC")
    return datetime.strptime(fecha, "%Y-%m-%d")


async def avisos_cap_ultimo_area(area: str, api_keys: Iterable[str]) -> dict:
    """Descarga los avisos CAP del ultimo elaborado para un area especifica.

    Args:
        area: Codigo del area (ver AREA_CODES).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Diccionario con los archivos extraidos {nombre: contenido}.

    Raises:
        ValueError: Si el area no es valida o no hay API keys.
        AemetError: Si hay error descargando los datos.
    """
    if not area or area not in AREA_CODES:
        raise ValueError(
            f"Codigo de area '{area}' no valido. Codigos validos: {', '.join(AREA_CODES)}"
        )

    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando avisos CAP para area %s (%s)", area, AREA_CODES[area])

    endpoint_template = (
        f"{BASE_URL}/api/avisos_cap/ultimoelaborado/area/{area}?api_key={{apiKey}}"
    )

    response = await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, tipo=f"avisos_cap_ultimo_{area}", api_keys=api_keys_list
    )

    if not isinstance(response, dict) or response.get("estado") != 200:
        raise AemetError(
            f"Error en AEMET: {response.get('descripcion', 'Error desconocido')} "
            f"(estado: {response.get('estado')})"
        )

    datos_url = response.get("datos")
    if not datos_url:
        raise AemetError("No se encontro URL de descarga en la respuesta de AEMET")

    logger.info("Descargando archivo CAP para area %s", area)
    return await descargar_archivo_tar_gz(datos_url)


async def avisos_cap_archivo(
    fecha_inicio: str,
    fecha_fin: str,
    api_keys: Iterable[str],
) -> dict:
    """Descarga el archivo de avisos CAP en un rango de fechas.

    Args:
        fecha_inicio: Fecha de inicio (AAAA-MM-DD o AAAA-MM-DDTHH:MM:SSUTC).
        fecha_fin: Fecha de fin (AAAA-MM-DD o AAAA-MM-DDTHH:MM:SSUTC).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Diccionario con todos los archivos extraidos del rango de fechas.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error descargando los datos.
    """
    api_keys_list = validar_api_keys(api_keys)

    if not fecha_inicio or not fecha_fin:
        raise ValueError("Los parametros 'fecha_inicio' y 'fecha_fin' son obligatorios.")

    fecha_inicio = _completar_fecha(fecha_inicio, inicio=True)
    fecha_fin = _completar_fecha(fecha_fin, inicio=False)

    dt_inicio = _parse_fecha(fecha_inicio)
    dt_fin = _parse_fecha(fecha_fin)

    if dt_inicio > dt_fin:
        raise ValueError("'fecha_inicio' no puede ser posterior a 'fecha_fin'.")

    todos_archivos: dict[str, str] = {}
    actual = dt_inicio
    while actual <= dt_fin:
        fecha_ini_str = actual.strftime("%Y-%m-%dT00:00:00UTC")
        fecha_fin_str = actual.strftime("%Y-%m-%dT23:59:59UTC")

        endpoint_template = (
            f"{BASE_URL}/api/avisos_cap/archivo/fechaini/{fecha_ini_str}"
            f"/fechafin/{fecha_fin_str}?api_key={{apiKey}}"
        )

        tipo = f"avisos_cap_archivo_{actual.strftime('%Y%m%d')}"
        logger.info("Solicitando avisos CAP archivo para %s", actual.strftime("%Y-%m-%d"))

        try:
            response = await fetch_con_reintentos_endpoint_aemet(
                endpoint_template, tipo=tipo, api_keys=api_keys_list
            )
            if isinstance(response, dict) and response.get("estado") == 200:
                datos_url = response.get("datos")
                if datos_url:
                    archivos = await descargar_archivo_tar_gz(datos_url)
                    todos_archivos.update(archivos)
            else:
                logger.warning(
                    "Sin datos para %s: %s",
                    actual.strftime("%Y-%m-%d"),
                    response.get("descripcion", ""),
                )
        except AemetError as exc:
            logger.warning("Error en avisos CAP para %s: %s", actual.strftime("%Y-%m-%d"), exc)

        actual += timedelta(days=1)

    return todos_archivos


async def avisos_vectorial_ultimo(api_keys: Iterable[str]) -> dict:
    """Descarga los avisos vectoriales del ultimo elaborado.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando avisos vectoriales ultimo elaborado")

    endpoint_template = (
        f"{BASE_URL}/api/avisos/vectorial/ultimoelaborado?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, tipo="avisos_vectorial_ultimo", api_keys=api_keys_list
    )
