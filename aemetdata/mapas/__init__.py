"""Modulo de mapas y graficos de AEMET."""

from __future__ import annotations

import logging
from typing import Iterable

from ..utils.suport_functions import (
    fetch_con_reintentos_endpoint_aemet,
    validar_api_keys,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://opendata.aemet.es/opendata"


async def analisis_ultimo(api_keys: Iterable[str]) -> dict:
    """Mapas de analisis. Ultima pasada.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando mapas de analisis ultima pasada")

    endpoint_template = (
        f"{BASE_URL}/api/mapasygraficos/analisis?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, "mapas_analisis", api_keys_list
    )


async def mapas_significativos(
    fecha: str,
    ambito: str,
    dia: str,
    api_keys: Iterable[str],
) -> dict:
    """Mapas significativos de tiempo actual o previsto.

    Args:
        fecha: Fecha de elaboracion (AAAA-MM-DD).
        ambito: Ambito: 'nacional' o 'ccaa'.
        dia: Periodo: 'D+0', 'D+1', 'D+2' con franja horaria (ej. '0-12', '12-24').
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error en la peticion.
    """
    if not fecha:
        raise ValueError("El parametro 'fecha' es obligatorio.")
    if ambito not in ("nacional", "ccaa"):
        raise ValueError("El parametro 'ambito' debe ser 'nacional' o 'ccaa'.")
    if not dia:
        raise ValueError("El parametro 'dia' es obligatorio.")

    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando mapas significativos fecha=%s ambito=%s dia=%s", fecha, ambito, dia)

    endpoint_template = (
        f"{BASE_URL}/api/mapasygraficos/mapassignificativos/fecha/{fecha}/{ambito}/{dia}?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"mapas_significativos_{fecha}_{ambito}_{dia}", api_keys_list
    )


async def mapas_previstos(alcance: str, api_keys: Iterable[str]) -> dict:
    """Mapas previstos. Ultima pasada.

    Args:
        alcance: Alcance de la prevision.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        ValueError: Si el alcance es invalido.
        AemetError: Si hay error en la peticion.
    """
    if not alcance:
        raise ValueError("El parametro 'alcance' es obligatorio.")

    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando mapas previstos alcance=%s", alcance)

    endpoint_template = (
        f"{BASE_URL}/api/mapasygraficos/previstos/{alcance}?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"mapas_previstos_{alcance}", api_keys_list
    )
