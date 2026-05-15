"""Modulo de redes de observacion de AEMET.

Incluye radar, rayos, ozono, contaminacion de fondo y radiacion.
"""

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


# ---------------------------------------------------------------------------
# Radar
# ---------------------------------------------------------------------------


async def radar_nacional(api_keys: Iterable[str]) -> bytes:
    """Imagen del radar nacional compuesto. Tiempo actual.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Bytes de la imagen de radar.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando radar nacional")

    endpoint_template = f"{BASE_URL}/api/red/radar/nacional?api_key={{apiKey}}"
    respuesta = await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, "radar_nacional", api_keys_list
    )

    url_imagen = respuesta.get("datos")
    if not url_imagen:
        return b""

    return await fetch_bytes_url(url_imagen, "radar_nacional")


async def radar_regional(producto: str, api_keys: Iterable[str]) -> bytes:
    """Imagen del radar regional. Tiempo actual.

    Args:
        producto: Codigo del producto de radar regional.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Bytes de la imagen de radar.

    Raises:
        ValueError: Si el producto es invalido.
        AemetError: Si hay error en la peticion.
    """
    if not producto:
        raise ValueError("El parametro 'producto' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando radar regional producto=%s", producto)

    endpoint_template = f"{BASE_URL}/api/red/radar/regional/{producto}?api_key={{apiKey}}"
    respuesta = await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"radar_regional_{producto}", api_keys_list
    )

    url_imagen = respuesta.get("datos")
    if not url_imagen:
        return b""

    return await fetch_bytes_url(url_imagen, f"radar_regional_{producto}")


# ---------------------------------------------------------------------------
# Rayos
# ---------------------------------------------------------------------------


async def rayos_mapa(api_keys: Iterable[str]) -> dict:
    """Mapa de rayos. Tiempo actual.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando mapa de rayos")

    endpoint_template = f"{BASE_URL}/api/red/rayos/mapa?api_key={{apiKey}}"
    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, "rayos_mapa", api_keys_list
    )


# ---------------------------------------------------------------------------
# Satelite
# ---------------------------------------------------------------------------


async def satelite_composicion_peninsula_peninsula(api_keys: Iterable[str]) -> dict:
    """Imagen de satelite de la Peninsula.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando imagen satelite Peninsula")

    endpoint_template = f"{BASE_URL}/api/red/satelite/componente/peninsula?api_key={{apiKey}}"
    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, "satelite_peninsula", api_keys_list
    )


# ---------------------------------------------------------------------------
# Contaminacion de fondo
# ---------------------------------------------------------------------------


async def contaminacion_fondo(estacion: str, magnitud: str, api_keys: Iterable[str]) -> dict:
    """Datos de contaminacion de fondo. Tiempo actual.

    Args:
        estacion: Codigo de estacion de contaminacion de fondo.
        magnitud: Codigo de magnitud a consultar.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        ValueError: Si los parametros son invalidos.
        AemetError: Si hay error en la peticion.
    """
    if not estacion or not magnitud:
        raise ValueError("Los parametros 'estacion' y 'magnitud' son obligatorios.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info(
        "Solicitando contaminacion de fondo estacion=%s magnitud=%s", estacion, magnitud
    )

    endpoint_template = (
        f"{BASE_URL}/api/red/especial/contaminacionfondo/estacion/{estacion}"
        f"/magnitud/{magnitud}?api_key={{apiKey}}"
    )
    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"contaminacion_fondo_{estacion}_{magnitud}", api_keys_list
    )


# ---------------------------------------------------------------------------
# Ozono
# ---------------------------------------------------------------------------


async def ozono(estacion: str, api_keys: Iterable[str]) -> dict:
    """Datos de ozono. Tiempo actual.

    Args:
        estacion: Codigo de estacion de ozono.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        ValueError: Si el parametro es invalido.
        AemetError: Si hay error en la peticion.
    """
    if not estacion:
        raise ValueError("El parametro 'estacion' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando datos de ozono estacion=%s", estacion)

    endpoint_template = (
        f"{BASE_URL}/api/red/especial/ozono/estacion/{estacion}?api_key={{apiKey}}"
    )
    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"ozono_{estacion}", api_keys_list
    )


async def perfil_ozono(estacion: str, api_keys: Iterable[str]) -> dict:
    """Perfil vertical de ozono. Tiempo actual.

    Args:
        estacion: Codigo de estacion de ozono.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.
    """
    if not estacion:
        raise ValueError("El parametro 'estacion' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando perfil de ozono estacion=%s", estacion)

    endpoint_template = (
        f"{BASE_URL}/api/red/especial/perfilozono/estacion/{estacion}?api_key={{apiKey}}"
    )
    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"perfil_ozono_{estacion}", api_keys_list
    )


# ---------------------------------------------------------------------------
# Radiacion
# ---------------------------------------------------------------------------


async def radiacion(estacion: str, magnitud: str, api_keys: Iterable[str]) -> dict:
    """Datos de radiacion solar. Tiempo actual.

    Args:
        estacion: Codigo de estacion de radiacion.
        magnitud: Codigo de magnitud a consultar.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.

    Raises:
        ValueError: Si los parametros son invalidos.
        AemetError: Si hay error en la peticion.
    """
    if not estacion or not magnitud:
        raise ValueError("Los parametros 'estacion' y 'magnitud' son obligatorios.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando radiacion estacion=%s magnitud=%s", estacion, magnitud)

    endpoint_template = (
        f"{BASE_URL}/api/red/especial/radiacion/estacion/{estacion}"
        f"/magnitud/{magnitud}?api_key={{apiKey}}"
    )
    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"radiacion_{estacion}_{magnitud}", api_keys_list
    )
