"""Modulo de modelos numericos de AEMET."""

from __future__ import annotations

import logging
from typing import Iterable

from ..utils.suport_functions import (
    fetch_con_reintentos_endpoint_aemet,
    validar_api_keys,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://opendata.aemet.es/opendata"


async def aespol(
    pasada: str,
    alcance: str,
    parametro: str,
    api_keys: Iterable[str],
) -> dict:
    """Modelo AESPOL de oleaje en el Atlantico Norte.

    Args:
        pasada: Pasada del modelo ('00' o '12').
        alcance: Alcance en horas ('00' a '48').
        parametro: Parametro ('hs', 'theta0', 'tmm10').
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error en la peticion.
    """
    if not pasada or not alcance or not parametro:
        raise ValueError("Los parametros 'pasada', 'alcance' y 'parametro' son obligatorios.")

    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando modelo AESPOL pasada=%s alcance=%s parametro=%s", pasada, alcance, parametro)

    endpoint_template = (
        f"{BASE_URL}/api/modelos/numericos/aespol/pasada/{pasada}/alcance/{alcance}"
        f"/parametro/{parametro}?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"modelo_aespol_{pasada}_{alcance}_{parametro}", api_keys_list
    )


async def aewam(
    pasada: str,
    alcance: str,
    parametro: str,
    api_keys: Iterable[str],
) -> dict:
    """Modelo AEWAM de oleaje atlantico.

    Args:
        pasada: Pasada del modelo ('00' o '12').
        alcance: Alcance en horas ('00' a '72').
        parametro: Parametro (shts, shww, swh, mdts, mdww, mwd, mpts, mpww, mwp).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error en la peticion.
    """
    if not pasada or not alcance or not parametro:
        raise ValueError("Los parametros 'pasada', 'alcance' y 'parametro' son obligatorios.")

    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando modelo AEWAM pasada=%s alcance=%s parametro=%s", pasada, alcance, parametro)

    endpoint_template = (
        f"{BASE_URL}/api/modelos/numericos/aewam/pasada/{pasada}/alcance/{alcance}"
        f"/parametro/{parametro}?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"modelo_aewam_{pasada}_{alcance}_{parametro}", api_keys_list
    )


async def harmonie_peninsula(
    pasada: str,
    alcance: str,
    parametro: str,
    formato: str,
    api_keys: Iterable[str],
) -> dict:
    """Modelo Harmonie para la Peninsula y Baleares.

    Args:
        pasada: Pasada del modelo ('00', '06', '12', '18').
        alcance: Alcance en horas ('00' a '72').
        parametro: Codigo de parametro (33, 61, 71, 207, 228, 117, 116, 6, 11).
        formato: Formato de salida ('grib' o 'netcdf').
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error en la peticion.
    """
    if not all([pasada, alcance, parametro, formato]):
        raise ValueError("Todos los parametros son obligatorios.")
    if formato not in ("grib", "netcdf"):
        raise ValueError("El parametro 'formato' debe ser 'grib' o 'netcdf'.")

    api_keys_list = validar_api_keys(api_keys)
    logger.info(
        "Solicitando modelo Harmonie Peninsula pasada=%s alcance=%s parametro=%s formato=%s",
        pasada, alcance, parametro, formato,
    )

    endpoint_template = (
        f"{BASE_URL}/api/modelos/numericos/harmonie/pb/pasada/{pasada}/alcance/{alcance}"
        f"/parametro/{parametro}/formato/{formato}?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template,
        f"modelo_harmonie_pb_{pasada}_{alcance}_{parametro}_{formato}",
        api_keys_list,
    )


async def harmonie_canarias(
    pasada: str,
    alcance: str,
    parametro: str,
    formato: str,
    api_keys: Iterable[str],
) -> dict:
    """Modelo Harmonie para Canarias.

    Args:
        pasada: Pasada del modelo ('00', '06', '12', '18').
        alcance: Alcance en horas ('00' a '72').
        parametro: Codigo de parametro (33, 61, 71, 207, 228, 117, 116, 6, 11).
        formato: Formato de salida ('grib' o 'netcdf').
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error en la peticion.
    """
    if not all([pasada, alcance, parametro, formato]):
        raise ValueError("Todos los parametros son obligatorios.")
    if formato not in ("grib", "netcdf"):
        raise ValueError("El parametro 'formato' debe ser 'grib' o 'netcdf'.")

    api_keys_list = validar_api_keys(api_keys)
    logger.info(
        "Solicitando modelo Harmonie Canarias pasada=%s alcance=%s parametro=%s formato=%s",
        pasada, alcance, parametro, formato,
    )

    endpoint_template = (
        f"{BASE_URL}/api/modelos/numericos/harmonie/can/pasada/{pasada}/alcance/{alcance}"
        f"/parametro/{parametro}/formato/{formato}?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template,
        f"modelo_harmonie_can_{pasada}_{alcance}_{parametro}_{formato}",
        api_keys_list,
    )
