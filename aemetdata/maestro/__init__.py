"""Modulo de datos maestros de AEMET (municipios)."""

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


async def todos_municipios(api_keys: Iterable[str]) -> list:
    """Devuelve todos los municipios de Espana.

    Util para obtener los codigos de municipio necesarios en predicciones.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de municipios con sus metadatos.

    Raises:
        AemetError: Si hay error en la peticion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando listado de todos los municipios")

    endpoint_template = (
        f"{BASE_URL}/api/maestro/municipios?api_key={{apiKey}}"
    )

    return await fetch_aemet_datos(endpoint_template, "maestro_municipios", api_keys_list)


async def municipio(codigo: str, api_keys: Iterable[str]) -> list:
    """Devuelve informacion de un municipio especifico por su codigo.

    Args:
        codigo: Codigo de municipio (ej. 'id28079' para Madrid).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos del municipio.

    Raises:
        ValueError: Si el codigo es invalido.
        AemetError: Si hay error en la peticion.
    """
    if not codigo:
        raise ValueError("El parametro 'codigo' es obligatorio.")

    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando datos del municipio %s", codigo)

    endpoint_template = (
        f"{BASE_URL}/api/maestro/municipio/{codigo}?api_key={{apiKey}}"
    )

    return await fetch_aemet_datos(
        endpoint_template, f"maestro_municipio_{codigo}", api_keys_list
    )


async def municipio_por_nombre(nombre: str, api_keys: Iterable[str]) -> list:
    """Busca municipios por nombre (busqueda parcial).

    Args:
        nombre: Nombre o parte del nombre del municipio.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de municipios que coinciden con el nombre.

    Raises:
        ValueError: Si el nombre es invalido.
        AemetError: Si hay error en la peticion.
    """
    if not nombre:
        raise ValueError("El parametro 'nombre' es obligatorio.")

    api_keys_list = validar_api_keys(api_keys)
    logger.info("Buscando municipios por nombre: %s", nombre)

    endpoint_template = (
        f"{BASE_URL}/api/maestro/municipio/nombre/{nombre}?api_key={{apiKey}}"
    )

    return await fetch_aemet_datos(
        endpoint_template, f"maestro_municipio_nombre_{nombre}", api_keys_list
    )
