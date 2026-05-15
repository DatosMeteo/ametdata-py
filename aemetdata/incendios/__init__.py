"""Modulo de indices de incendios forestales de AEMET."""

from __future__ import annotations

import logging
from typing import Iterable

from ..utils.suport_functions import (
    AemetError,
    fetch_aemet_datos,
    fetch_con_reintentos_endpoint_aemet,
    validar_api_keys,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://opendata.aemet.es/opendata"

# Areas validas
AREAS_INCENDIOS = {
    "p": "Peninsula",
    "b": "Baleares",
    "c": "Canarias",
}


def _validar_area(area: str) -> None:
    if area not in AREAS_INCENDIOS:
        raise ValueError(
            f"Area '{area}' no valida. Opciones: {', '.join(AREAS_INCENDIOS)} "
            f"(p=Peninsula, b=Baleares, c=Canarias)"
        )


async def mapa_riesgo_estimado(area: str, api_keys: Iterable[str]) -> dict:
    """Mapa de niveles de riesgo estimado meteorologico de incendios forestales.

    Args:
        area: Codigo de area: 'p' (Peninsula), 'b' (Baleares), 'c' (Canarias).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        ValueError: Si el area no es valida.
        AemetError: Si hay error en la peticion.
    """
    _validar_area(area)
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando mapa riesgo estimado incendios area %s", area)

    endpoint_template = (
        f"{BASE_URL}/api/incendios/mapasriesgo/estimado/area/{area}?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"incendios_estimado_{area}", api_keys_list
    )


async def mapa_riesgo_previsto(dia: str, area: str, api_keys: Iterable[str]) -> dict:
    """Mapa de niveles de riesgo previsto meteorologico de incendios forestales.

    Args:
        dia: Dia de prevision: '1' (manana), '2' (pasado manana), '3' (dentro de 3 dias).
        area: Codigo de area: 'p' (Peninsula), 'b' (Baleares), 'c' (Canarias).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error en la peticion.
    """
    if str(dia) not in ("1", "2", "3"):
        raise ValueError("El parametro 'dia' debe ser '1', '2' o '3'.")
    _validar_area(area)
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando mapa riesgo previsto incendios dia=%s area=%s", dia, area)

    endpoint_template = (
        f"{BASE_URL}/api/incendios/mapasriesgo/previsto/dia/{dia}/area/{area}?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"incendios_previsto_{dia}_{area}", api_keys_list
    )


async def riesgo_raster(api_keys: Iterable[str]) -> dict:
    """Raster de niveles de riesgo previsto meteorologico de incendios forestales.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando raster de riesgo incendios")

    endpoint_template = (
        f"{BASE_URL}/api/incendios/riesgo/raster?api_key={{apiKey}}"
    )

    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, "incendios_raster", api_keys_list
    )
