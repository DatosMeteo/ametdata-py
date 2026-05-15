"""Modulo de imagenes y productos graficos de AEMET."""

from __future__ import annotations

import logging
from typing import Iterable

from ..utils.suport_functions import (
    fetch_bytes_url,
    fetch_con_reintentos_endpoint_aemet,
    validar_api_keys,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://opendata.aemet.es/opendata"


async def satelite_ndvi(api_keys: Iterable[str]) -> bytes:
    """Imagen de indice de vegetacion NDVI del satelite.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Bytes de la imagen NDVI.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando imagen NDVI satelite")

    endpoint_template = f"{BASE_URL}/api/satelites/producto/nvdi?api_key={{apiKey}}"
    respuesta = await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, "satelite_ndvi", api_keys_list
    )

    url_imagen = respuesta.get("datos")
    if not url_imagen:
        return b""

    return await fetch_bytes_url(url_imagen, "satelite_ndvi")


async def satelite_sst(api_keys: Iterable[str]) -> bytes:
    """Imagen de temperatura superficial del mar (SST) del satelite.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Bytes de la imagen SST.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando imagen SST satelite")

    endpoint_template = f"{BASE_URL}/api/satelites/producto/sst?api_key={{apiKey}}"
    respuesta = await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, "satelite_sst", api_keys_list
    )

    url_imagen = respuesta.get("datos")
    if not url_imagen:
        return b""

    return await fetch_bytes_url(url_imagen, "satelite_sst")
