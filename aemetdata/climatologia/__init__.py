"""Modulo de climatologia de AEMET.

Descarga datos climatologicos: mensuales, diarios, horarios, extremos, normales,
inventario de estaciones, rejillas y productos georreferenciados.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta
from typing import Iterable

from ..utils.suport_functions import (
    AemetError,
    fetch_aemet_datos,
    fetch_con_reintentos_endpoint_aemet,
    get_relativedelta,
    normalizar_datos,
    procesar_lista_ids,
    validar_api_keys,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://opendata.aemet.es/opendata"

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


def _generar_intervalos_mensuales(dt_inicio: datetime, dt_fin: datetime) -> list:
    """Genera intervalos de ~6 meses para peticiones a la API."""
    relativedelta = get_relativedelta()
    intervalos = []
    actual = dt_inicio
    while actual <= dt_fin:
        siguiente = actual + relativedelta(months=5, days=29)
        if siguiente > dt_fin:
            siguiente = dt_fin
        intervalos.append((actual, siguiente))
        actual = siguiente + timedelta(days=1)
    return intervalos


async def datos_mensuales(
    idema: str | Iterable[str],
    anio_inicio: int,
    anio_fin: int,
    api_keys: Iterable[str],
) -> list:
    """Descarga climatologias mensuales por estacion y rango de anios.

    Args:
        idema: Identificador IDEMA o lista de identificadores.
        anio_inicio: Anio inicial (incluido).
        anio_fin: Anio final (incluido).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de registros climatologicos.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error descargando los datos.
    """
    idemas = procesar_lista_ids(idema)
    api_keys_list = validar_api_keys(api_keys)

    if not isinstance(anio_inicio, int) or not isinstance(anio_fin, int):
        raise ValueError("'anio_inicio' y 'anio_fin' deben ser enteros.")
    if anio_inicio > anio_fin:
        raise ValueError("'anio_inicio' no puede ser mayor que 'anio_fin'.")

    all_results: list = []
    for idema_item in idemas:
        anio_ini = anio_inicio
        while anio_ini <= anio_fin:
            anio_fin_intervalo = min(anio_ini + 2, anio_fin)
            endpoint_template = (
                f"{BASE_URL}/api/valores/climatologicos/mensualesanuales/datos/"
                f"anioini/{anio_ini}/aniofin/{anio_fin_intervalo}/"
                f"estacion/{idema_item}?api_key={{apiKey}}"
            )
            tipo = f"clima_mensual_{idema_item}_{anio_ini}_{anio_fin_intervalo}"
            logger.info(
                "Solicitando climatologia mensual para %s entre %d y %d",
                idema_item, anio_ini, anio_fin_intervalo,
            )
            datos = await fetch_aemet_datos(endpoint_template, tipo, api_keys_list)
            all_results.extend(datos)
            anio_ini = anio_fin_intervalo + 1

    return all_results


async def datos_diarios(
    idema: str | Iterable[str],
    fecha_inicio: str,
    fecha_fin: str,
    api_keys: Iterable[str],
) -> list:
    """Descarga climatologias diarias por estacion y rango de fechas.

    Args:
        idema: Identificador IDEMA o lista de identificadores.
        fecha_inicio: Fecha inicial (AAAA-MM-DD o AAAA-MM-DDTHH:MM:SSUTC).
        fecha_fin: Fecha final (AAAA-MM-DD o AAAA-MM-DDTHH:MM:SSUTC).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de registros climatologicos.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error descargando los datos.
    """
    idemas = procesar_lista_ids(idema)
    api_keys_list = validar_api_keys(api_keys)

    fecha_inicio = _completar_fecha(fecha_inicio, inicio=True)
    fecha_fin = _completar_fecha(fecha_fin, inicio=False)
    dt_inicio = _parse_fecha(fecha_inicio)
    dt_fin = _parse_fecha(fecha_fin)
    intervalos = _generar_intervalos_mensuales(dt_inicio, dt_fin)

    all_results: list = []
    for idema_item in idemas:
        for ini, fin in intervalos:
            fecha_ini_str = ini.strftime("%Y-%m-%dT00:00:00UTC")
            fecha_fin_str = fin.strftime("%Y-%m-%dT23:59:59UTC")
            endpoint_template = (
                f"{BASE_URL}/api/valores/climatologicos/diarios/datos/"
                f"fechaini/{fecha_ini_str}/fechafin/{fecha_fin_str}/"
                f"estacion/{idema_item}?api_key={{apiKey}}"
            )
            tipo = f"clima_diario_{idema_item}_{fecha_ini_str[:10]}_{fecha_fin_str[:10]}"
            logger.info(
                "Solicitando climatologia diaria para %s entre %s y %s",
                idema_item, fecha_ini_str, fecha_fin_str,
            )
            datos = await fetch_aemet_datos(endpoint_template, tipo, api_keys_list)
            all_results.extend(datos)

    return all_results


async def datos_diarios_todas_estaciones(
    fecha_inicio: str,
    fecha_fin: str,
    api_keys: Iterable[str],
) -> list:
    """Descarga climatologias diarias de todas las estaciones para un rango de fechas.

    Args:
        fecha_inicio: Fecha inicial (AAAA-MM-DD o AAAA-MM-DDTHH:MM:SSUTC).
        fecha_fin: Fecha final (AAAA-MM-DD o AAAA-MM-DDTHH:MM:SSUTC).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de registros climatologicos.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error descargando los datos.
    """
    api_keys_list = validar_api_keys(api_keys)

    fecha_inicio = _completar_fecha(fecha_inicio, inicio=True)
    fecha_fin = _completar_fecha(fecha_fin, inicio=False)
    dt_inicio = _parse_fecha(fecha_inicio)
    dt_fin = _parse_fecha(fecha_fin)
    intervalos = _generar_intervalos_mensuales(dt_inicio, dt_fin)

    all_results: list = []
    for ini, fin in intervalos:
        fecha_ini_str = ini.strftime("%Y-%m-%dT00:00:00UTC")
        fecha_fin_str = fin.strftime("%Y-%m-%dT23:59:59UTC")
        endpoint_template = (
            f"{BASE_URL}/api/valores/climatologicos/diarios/datos/"
            f"fechaini/{fecha_ini_str}/fechafin/{fecha_fin_str}/"
            f"todasestaciones?api_key={{apiKey}}"
        )
        tipo = f"clima_diario_todas_{fecha_ini_str[:10]}_{fecha_fin_str[:10]}"
        logger.info(
            "Solicitando climatologia diaria todas las estaciones entre %s y %s",
            fecha_ini_str, fecha_fin_str,
        )
        datos = await fetch_aemet_datos(endpoint_template, tipo, api_keys_list)
        all_results.extend(datos)

    return all_results


async def datos_horarios(
    idema: str | Iterable[str],
    fecha_inicio: str,
    fecha_fin: str,
    api_keys: Iterable[str],
) -> list:
    """Descarga climatologias horarias por estacion y rango de fechas.

    Args:
        idema: Identificador IDEMA o lista de identificadores.
        fecha_inicio: Fecha inicial (AAAA-MM-DD o AAAA-MM-DDTHH:MM:SSUTC).
        fecha_fin: Fecha final (AAAA-MM-DD o AAAA-MM-DDTHH:MM:SSUTC).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de registros horarios.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error descargando los datos.
    """
    idemas = procesar_lista_ids(idema)
    api_keys_list = validar_api_keys(api_keys)

    fecha_inicio = _completar_fecha(fecha_inicio, inicio=True)
    fecha_fin = _completar_fecha(fecha_fin, inicio=False)
    dt_inicio = _parse_fecha(fecha_inicio)
    dt_fin = _parse_fecha(fecha_fin)
    intervalos = _generar_intervalos_mensuales(dt_inicio, dt_fin)

    all_results: list = []
    for idema_item in idemas:
        for ini, fin in intervalos:
            fecha_ini_str = ini.strftime("%Y-%m-%dT00:00:00UTC")
            fecha_fin_str = fin.strftime("%Y-%m-%dT23:59:59UTC")
            endpoint_template = (
                f"{BASE_URL}/api/valores/climatologicos/horarios/datos/"
                f"fechaini/{fecha_ini_str}/fechafin/{fecha_fin_str}/"
                f"estacion/{idema_item}?api_key={{apiKey}}"
            )
            tipo = f"clima_horario_{idema_item}_{fecha_ini_str[:10]}_{fecha_fin_str[:10]}"
            logger.info(
                "Solicitando climatologia horaria para %s entre %s y %s",
                idema_item, fecha_ini_str, fecha_fin_str,
            )
            datos = await fetch_aemet_datos(endpoint_template, tipo, api_keys_list)
            all_results.extend(datos)

    return all_results


async def datos_horarios_todas_estaciones(
    fecha_inicio: str,
    fecha_fin: str,
    api_keys: Iterable[str],
) -> list:
    """Descarga climatologias horarias de todas las estaciones para un rango de fechas.

    Args:
        fecha_inicio: Fecha inicial (AAAA-MM-DD o AAAA-MM-DDTHH:MM:SSUTC).
        fecha_fin: Fecha final (AAAA-MM-DD o AAAA-MM-DDTHH:MM:SSUTC).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de registros horarios.
    """
    api_keys_list = validar_api_keys(api_keys)

    fecha_inicio = _completar_fecha(fecha_inicio, inicio=True)
    fecha_fin = _completar_fecha(fecha_fin, inicio=False)
    dt_inicio = _parse_fecha(fecha_inicio)
    dt_fin = _parse_fecha(fecha_fin)
    intervalos = _generar_intervalos_mensuales(dt_inicio, dt_fin)

    all_results: list = []
    for ini, fin in intervalos:
        fecha_ini_str = ini.strftime("%Y-%m-%dT00:00:00UTC")
        fecha_fin_str = fin.strftime("%Y-%m-%dT23:59:59UTC")
        endpoint_template = (
            f"{BASE_URL}/api/valores/climatologicos/horarios/datos/"
            f"fechaini/{fecha_ini_str}/fechafin/{fecha_fin_str}/"
            f"todasestaciones?api_key={{apiKey}}"
        )
        tipo = f"clima_horario_todas_{fecha_ini_str[:10]}_{fecha_fin_str[:10]}"
        logger.info(
            "Solicitando climatologia horaria todas las estaciones entre %s y %s",
            fecha_ini_str, fecha_fin_str,
        )
        datos = await fetch_aemet_datos(endpoint_template, tipo, api_keys_list)
        all_results.extend(datos)

    return all_results


async def datos_extremos(
    idema: str | Iterable[str],
    api_keys: Iterable[str],
    parametro: str | Iterable[str] | None = None,
) -> list:
    """Descarga valores extremos climatologicos por estacion y parametros.

    Args:
        idema: Identificador IDEMA o lista de identificadores.
        api_keys: Iterable con las claves API de AEMET.
        parametro: 'P' (precipitacion), 'T' (temperatura), 'V' (viento).
                   Por defecto usa todos.

    Returns:
        Lista de registros de valores extremos.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error descargando los datos.
    """
    if parametro is None:
        parametros = ["P", "T", "V"]
    elif isinstance(parametro, str):
        parametros = [parametro]
    elif isinstance(parametro, (list, tuple)):
        parametros = list(parametro)
    else:
        raise ValueError("'parametro' debe ser str o iterable de str.")

    idemas = procesar_lista_ids(idema)
    api_keys_list = validar_api_keys(api_keys)

    all_results: list = []
    for idema_item in idemas:
        for param in parametros:
            endpoint_template = (
                f"{BASE_URL}/api/valores/climatologicos/valoresextremos/"
                f"parametro/{param}/estacion/{idema_item}?api_key={{apiKey}}"
            )
            tipo = f"clima_extremos_{idema_item}_{param}"
            logger.info(
                "Solicitando valores extremos para %s, parametro %s",
                idema_item, param,
            )
            datos = await fetch_aemet_datos(endpoint_template, tipo, api_keys_list)
            all_results.extend(datos)

    return all_results


async def datos_normales(
    idema: str | Iterable[str],
    api_keys: Iterable[str],
) -> list:
    """Descarga climatologias normales (1981-2010) por estacion.

    Args:
        idema: Identificador IDEMA o lista de identificadores.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de registros de valores normales.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error descargando los datos.
    """
    idemas = procesar_lista_ids(idema)
    api_keys_list = validar_api_keys(api_keys)

    all_results: list = []
    for idema_item in idemas:
        endpoint_template = (
            f"{BASE_URL}/api/valores/climatologicos/normales/estacion/{idema_item}?api_key={{apiKey}}"
        )
        tipo = f"clima_normales_{idema_item}"
        logger.info("Solicitando valores normales para %s", idema_item)
        datos = await fetch_aemet_datos(endpoint_template, tipo, api_keys_list)
        all_results.extend(datos)

    return all_results


async def inventario_estaciones(api_keys: Iterable[str]) -> list:
    """Descarga el inventario completo de estaciones climatologicas.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de estaciones con sus metadatos.

    Raises:
        AemetError: Si hay error descargando los datos.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando inventario completo de estaciones")

    endpoint_template = (
        f"{BASE_URL}/api/valores/climatologicos/inventarioestaciones/todasestaciones?api_key={{apiKey}}"
    )

    return await fetch_aemet_datos(endpoint_template, "inventario_estaciones", api_keys_list)


async def inventario_estaciones_por_id(
    estaciones: str | Iterable[str],
    api_keys: Iterable[str],
) -> list:
    """Descarga el inventario de estaciones por indicativo climatologico.

    Args:
        estaciones: Identificador o lista de identificadores (IDEMA).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de estaciones con sus metadatos.

    Raises:
        AemetError: Si hay error descargando los datos.
    """
    ids = procesar_lista_ids(estaciones, "estaciones")
    api_keys_list = validar_api_keys(api_keys)

    ids_str = ",".join(ids)
    logger.info("Solicitando inventario para estaciones: %s", ids_str)

    endpoint_template = (
        f"{BASE_URL}/api/valores/climatologicos/inventarioestaciones/estaciones/{ids_str}?api_key={{apiKey}}"
    )

    return await fetch_aemet_datos(
        endpoint_template, f"inventario_estaciones_{ids_str}", api_keys_list
    )


async def rejillas_anuales(
    area: str,
    parametro: str,
    anio: str | int,
    api_keys: Iterable[str],
) -> list:
    """Descarga la observacion en rejillas anuales.

    Args:
        area: Codigo de area (ej. 'esp').
        parametro: Nombre del parametro meteorologico.
        anio: Anio (AAAA).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de registros.

    Raises:
        AemetError: Si hay error descargando los datos.
    """
    api_keys_list = validar_api_keys(api_keys)
    anio_str = str(anio)
    logger.info("Solicitando rejillas anuales area=%s parametro=%s anio=%s", area, parametro, anio_str)

    endpoint_template = (
        f"{BASE_URL}/api/valores/climatologicos/observacionrejillas/anuales/"
        f"area/{area}/parametro/{parametro}/{anio_str}?api_key={{apiKey}}"
    )

    return await fetch_aemet_datos(
        endpoint_template, f"rejillas_anuales_{area}_{parametro}_{anio_str}", api_keys_list
    )


async def rejillas_mensuales(
    area: str,
    parametro: str,
    anio: str | int,
    mes: str | int,
    api_keys: Iterable[str],
) -> list:
    """Descarga la observacion en rejillas mensuales.

    Args:
        area: Codigo de area (ej. 'esp').
        parametro: Nombre del parametro meteorologico.
        anio: Anio (AAAA).
        mes: Mes (MM).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de registros.

    Raises:
        AemetError: Si hay error descargando los datos.
    """
    api_keys_list = validar_api_keys(api_keys)
    anio_str = str(anio)
    mes_str = str(mes).zfill(2)
    logger.info(
        "Solicitando rejillas mensuales area=%s parametro=%s anio=%s mes=%s",
        area, parametro, anio_str, mes_str,
    )

    endpoint_template = (
        f"{BASE_URL}/api/valores/climatologicos/observacionrejillas/mensuales/"
        f"area/{area}/parametro/{parametro}/{anio_str}/{mes_str}?api_key={{apiKey}}"
    )

    return await fetch_aemet_datos(
        endpoint_template, f"rejillas_mensuales_{area}_{parametro}_{anio_str}_{mes_str}", api_keys_list
    )


async def raster_normales(api_keys: Iterable[str]) -> dict:
    """Descarga los valores normales georreferenciados.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando valores normales georreferenciados")

    endpoint_template = (
        f"{BASE_URL}/api/valores/climatologicos/raster/normales?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, "raster_normales", api_keys_list
    )


async def superacion_umbrales(api_keys: Iterable[str]) -> dict:
    """Descarga los valores normales (umbrales) georreferenciados.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando superacion de umbrales georreferenciados")

    endpoint_template = (
        f"{BASE_URL}/api/valores/climatologicos/vectorial/superacionumbrales?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, "superacion_umbrales", api_keys_list
    )
