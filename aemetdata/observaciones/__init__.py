"""Modulo de observacion convencional de AEMET.

Descarga datos de observacion de estaciones meteorologicas convencionales.
"""

from __future__ import annotations

import logging
from typing import Iterable

from ..utils.suport_functions import (
    AemetError,
    fetch_aemet_datos,
    fetch_con_reintentos_endpoint_aemet,
    procesar_lista_ids,
    validar_api_keys,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://opendata.aemet.es/opendata"


async def todas(api_keys: Iterable[str]) -> list:
    """Datos de observacion de todas las estaciones. Ultimas 24 horas.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de observaciones.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando observaciones de todas las estaciones (24h)")

    endpoint_template = (
        f"{BASE_URL}/api/observacion/convencional/todas?api_key={{apiKey}}"
    )

    return await fetch_aemet_datos(endpoint_template, "obs_todas", api_keys_list)


async def datos_estacion(idema: str | Iterable[str], api_keys: Iterable[str]) -> list:
    """Datos de observacion de una o varias estaciones. Tiempo actual.

    Args:
        idema: Identificador IDEMA o lista de identificadores.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de observaciones.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    idemas = procesar_lista_ids(idema)
    api_keys_list = validar_api_keys(api_keys)

    all_results: list = []
    for idema_item in idemas:
        logger.info("Solicitando observacion de estacion %s", idema_item)
        endpoint_template = (
            f"{BASE_URL}/api/observacion/convencional/datos/estacion/{idema_item}?api_key={{apiKey}}"
        )
        datos = await fetch_aemet_datos(
            endpoint_template, f"obs_estacion_{idema_item}", api_keys_list
        )
        all_results.extend(datos)

    return all_results


async def diezminutal_todas(api_keys: Iterable[str]) -> list:
    """Datos de observacion cada 10 minutos de todas las estaciones. Ultima hora.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de observaciones diezminutales.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando observaciones diezminutales de todas las estaciones")

    endpoint_template = (
        f"{BASE_URL}/api/observacion/convencional/diezminutal/todas?api_key={{apiKey}}"
    )

    return await fetch_aemet_datos(endpoint_template, "obs_diezminutal_todas", api_keys_list)


async def diezminutal_estacion(idema: str | Iterable[str], api_keys: Iterable[str]) -> list:
    """Datos de observacion cada 10 minutos por estacion. Ultima hora.

    Args:
        idema: Identificador IDEMA o lista de identificadores.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de observaciones diezminutales.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    idemas = procesar_lista_ids(idema)
    api_keys_list = validar_api_keys(api_keys)

    all_results: list = []
    for idema_item in idemas:
        logger.info("Solicitando observacion diezminutal de estacion %s", idema_item)
        endpoint_template = (
            f"{BASE_URL}/api/observacion/convencional/diezminutal/datos/estacion/{idema_item}?api_key={{apiKey}}"
        )
        datos = await fetch_aemet_datos(
            endpoint_template, f"obs_diezminutal_{idema_item}", api_keys_list
        )
        all_results.extend(datos)

    return all_results


async def diezminutal_fecha_estacion(
    fecha: str,
    idema: str | Iterable[str],
    api_keys: Iterable[str],
) -> list:
    """Datos de observacion cada 10 minutos por estacion en una fecha. Ultima hora.

    Args:
        fecha: Fecha en formato AAAA-MM-DD.
        idema: Identificador IDEMA o lista de identificadores.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de observaciones diezminutales.

    Raises:
        ValueError: Si la fecha no es valida.
        AemetError: Si hay error en la peticion.
    """
    if not fecha:
        raise ValueError("El parametro 'fecha' es obligatorio.")

    idemas = procesar_lista_ids(idema)
    api_keys_list = validar_api_keys(api_keys)

    all_results: list = []
    for idema_item in idemas:
        logger.info(
            "Solicitando observacion diezminutal de estacion %s para fecha %s",
            idema_item, fecha,
        )
        endpoint_template = (
            f"{BASE_URL}/api/observacion/convencional/diezminutal/datos/"
            f"fecha/{fecha}/estacion/{idema_item}?api_key={{apiKey}}"
        )
        datos = await fetch_aemet_datos(
            endpoint_template, f"obs_diezminutal_fecha_{idema_item}_{fecha}", api_keys_list
        )
        all_results.extend(datos)

    return all_results


async def diezminutal_ccaa(ccaa: str, api_keys: Iterable[str]) -> list:
    """Datos de observacion cada 10 minutos de todas las estaciones de una CCAA. Ultima hora.

    Args:
        ccaa: Codigo de comunidad autonoma.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de observaciones diezminutales.

    Raises:
        ValueError: Si el codigo de CCAA es invalido.
        AemetError: Si hay error en la peticion.
    """
    if not ccaa:
        raise ValueError("El parametro 'ccaa' es obligatorio.")

    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando observaciones diezminutales para CCAA %s", ccaa)

    endpoint_template = (
        f"{BASE_URL}/api/observacion/convencional/diezminutal/ccaa/{ccaa}?api_key={{apiKey}}"
    )

    return await fetch_aemet_datos(
        endpoint_template, f"obs_diezminutal_ccaa_{ccaa}", api_keys_list
    )


async def mensajes_tipo(tipomensaje: str, api_keys: Iterable[str]) -> list:
    """Ultimos mensajes de observacion por tipo de mensaje.

    Args:
        tipomensaje: Tipo de mensaje (ej. 'SYNOP', 'TEMP', etc.).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de mensajes.

    Raises:
        ValueError: Si el tipo de mensaje es invalido.
        AemetError: Si hay error en la peticion.
    """
    if not tipomensaje:
        raise ValueError("El parametro 'tipomensaje' es obligatorio.")

    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando mensajes de observacion tipo %s", tipomensaje)

    endpoint_template = (
        f"{BASE_URL}/api/observacion/convencional/mensajes/tipomensaje/{tipomensaje}?api_key={{apiKey}}"
    )

    return await fetch_aemet_datos(
        endpoint_template, f"obs_mensajes_{tipomensaje}", api_keys_list
    )


