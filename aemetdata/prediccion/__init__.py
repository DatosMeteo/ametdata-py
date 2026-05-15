"""Modulo de predicciones de AEMET.

Incluye predicciones nacionales, de CCAA, de provincia, de municipio,
maritimas, especificas y georreferenciadas.
"""

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


# ---------------------------------------------------------------------------
# Prediccion nacional
# ---------------------------------------------------------------------------


async def nacional_hoy(api_keys: Iterable[str]) -> list:
    """Prediccion nacional para hoy. Tiempo actual.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion nacional hoy")

    endpoint_template = f"{BASE_URL}/api/prediccion/nacional/hoy?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, "pred_nacional_hoy", api_keys_list)


async def nacional_hoy_archivo(fecha: str, api_keys: Iterable[str]) -> list:
    """Prediccion nacional para hoy. Archivo por fecha de elaboracion.

    Args:
        fecha: Dia de elaboracion (AAAA-MM-DD).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    if not fecha:
        raise ValueError("El parametro 'fecha' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion nacional hoy archivo fecha=%s", fecha)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/nacional/hoy/elaboracion/{fecha}?api_key={{apiKey}}"
    )
    return await fetch_aemet_datos(endpoint_template, f"pred_nacional_hoy_{fecha}", api_keys_list)


async def nacional_manana(api_keys: Iterable[str]) -> list:
    """Prediccion nacional para manana. Tiempo actual.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion nacional manana")

    endpoint_template = f"{BASE_URL}/api/prediccion/nacional/manana?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, "pred_nacional_manana", api_keys_list)


async def nacional_manana_archivo(fecha: str, api_keys: Iterable[str]) -> list:
    """Prediccion nacional para manana. Archivo por fecha de elaboracion."""
    if not fecha:
        raise ValueError("El parametro 'fecha' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion nacional manana archivo fecha=%s", fecha)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/nacional/manana/elaboracion/{fecha}?api_key={{apiKey}}"
    )
    return await fetch_aemet_datos(endpoint_template, f"pred_nacional_manana_{fecha}", api_keys_list)


async def nacional_pasadomanana(api_keys: Iterable[str]) -> list:
    """Prediccion nacional para pasado manana. Tiempo actual."""
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion nacional pasado manana")

    endpoint_template = f"{BASE_URL}/api/prediccion/nacional/pasadomanana?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, "pred_nacional_pasadomanana", api_keys_list)


async def nacional_medioplazo(api_keys: Iterable[str]) -> list:
    """Prediccion nacional a medio plazo. Tiempo actual."""
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion nacional medio plazo")

    endpoint_template = f"{BASE_URL}/api/prediccion/nacional/medioplazo?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, "pred_nacional_medioplazo", api_keys_list)


async def nacional_tendencia(api_keys: Iterable[str]) -> list:
    """Prediccion nacional de tendencia. Tiempo actual."""
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion nacional tendencia")

    endpoint_template = f"{BASE_URL}/api/prediccion/nacional/tendencia?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, "pred_nacional_tendencia", api_keys_list)


# ---------------------------------------------------------------------------
# Prediccion de CCAA
# ---------------------------------------------------------------------------


async def ccaa_hoy(ccaa: str, api_keys: Iterable[str]) -> list:
    """Prediccion de CCAA para hoy. Tiempo actual.

    Args:
        ccaa: Codigo de comunidad autonoma.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    if not ccaa:
        raise ValueError("El parametro 'ccaa' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion CCAA hoy ccaa=%s", ccaa)

    endpoint_template = f"{BASE_URL}/api/prediccion/ccaa/hoy/{ccaa}?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, f"pred_ccaa_hoy_{ccaa}", api_keys_list)


async def ccaa_hoy_archivo(ccaa: str, fecha: str, api_keys: Iterable[str]) -> list:
    """Prediccion de CCAA para hoy. Archivo por fecha de elaboracion."""
    if not ccaa or not fecha:
        raise ValueError("Los parametros 'ccaa' y 'fecha' son obligatorios.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion CCAA hoy ccaa=%s fecha=%s", ccaa, fecha)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/ccaa/hoy/{ccaa}/elaboracion/{fecha}?api_key={{apiKey}}"
    )
    return await fetch_aemet_datos(endpoint_template, f"pred_ccaa_hoy_{ccaa}_{fecha}", api_keys_list)


async def ccaa_manana(ccaa: str, api_keys: Iterable[str]) -> list:
    """Prediccion de CCAA para manana. Tiempo actual."""
    if not ccaa:
        raise ValueError("El parametro 'ccaa' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion CCAA manana ccaa=%s", ccaa)

    endpoint_template = f"{BASE_URL}/api/prediccion/ccaa/manana/{ccaa}?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, f"pred_ccaa_manana_{ccaa}", api_keys_list)


async def ccaa_pasadomanana(ccaa: str, api_keys: Iterable[str]) -> list:
    """Prediccion de CCAA para pasado manana. Tiempo actual."""
    if not ccaa:
        raise ValueError("El parametro 'ccaa' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion CCAA pasado manana ccaa=%s", ccaa)

    endpoint_template = f"{BASE_URL}/api/prediccion/ccaa/pasadomanana/{ccaa}?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, f"pred_ccaa_pasadomanana_{ccaa}", api_keys_list)


async def ccaa_medioplazo(ccaa: str, api_keys: Iterable[str]) -> list:
    """Prediccion de CCAA a medio plazo. Tiempo actual."""
    if not ccaa:
        raise ValueError("El parametro 'ccaa' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion CCAA medio plazo ccaa=%s", ccaa)

    endpoint_template = f"{BASE_URL}/api/prediccion/ccaa/medioplazo/{ccaa}?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, f"pred_ccaa_medioplazo_{ccaa}", api_keys_list)


# ---------------------------------------------------------------------------
# Prediccion de provincia
# ---------------------------------------------------------------------------


async def provincia_hoy(provincia: str, api_keys: Iterable[str]) -> list:
    """Prediccion de provincia para hoy. Tiempo actual.

    Args:
        provincia: Codigo de provincia.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    if not provincia:
        raise ValueError("El parametro 'provincia' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion provincia hoy provincia=%s", provincia)

    endpoint_template = f"{BASE_URL}/api/prediccion/provincia/hoy/{provincia}?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, f"pred_provincia_hoy_{provincia}", api_keys_list)


async def provincia_manana(provincia: str, api_keys: Iterable[str]) -> list:
    """Prediccion de provincia para manana. Tiempo actual."""
    if not provincia:
        raise ValueError("El parametro 'provincia' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion provincia manana provincia=%s", provincia)

    endpoint_template = f"{BASE_URL}/api/prediccion/provincia/manana/{provincia}?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, f"pred_provincia_manana_{provincia}", api_keys_list)


# ---------------------------------------------------------------------------
# Prediccion especifica de municipio
# ---------------------------------------------------------------------------


async def municipio_diaria(municipio: str, api_keys: Iterable[str]) -> list:
    """Prediccion diaria por municipio. Tiempo actual.

    Args:
        municipio: Codigo de municipio (ej. '28079' para Madrid).
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    if not municipio:
        raise ValueError("El parametro 'municipio' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion diaria para municipio %s", municipio)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/especifica/municipio/diaria/{municipio}?api_key={{apiKey}}"
    )
    return await fetch_aemet_datos(endpoint_template, f"pred_municipio_diaria_{municipio}", api_keys_list)


async def municipio_horaria(municipio: str, api_keys: Iterable[str]) -> list:
    """Prediccion horaria por municipio. Tiempo actual.

    Args:
        municipio: Codigo de municipio.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    if not municipio:
        raise ValueError("El parametro 'municipio' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion horaria para municipio %s", municipio)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/especifica/municipio/horaria/{municipio}?api_key={{apiKey}}"
    )
    return await fetch_aemet_datos(endpoint_template, f"pred_municipio_horaria_{municipio}", api_keys_list)


# ---------------------------------------------------------------------------
# Prediccion especifica de playa
# ---------------------------------------------------------------------------


async def playa(codigo_playa: str, api_keys: Iterable[str]) -> list:
    """Prediccion para playas. Tiempo actual.

    Args:
        codigo_playa: Codigo de playa.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    if not codigo_playa:
        raise ValueError("El parametro 'codigo_playa' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion para playa %s", codigo_playa)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/especifica/playa/{codigo_playa}?api_key={{apiKey}}"
    )
    return await fetch_aemet_datos(
        endpoint_template, f"pred_playa_{codigo_playa}", api_keys_list
    )


# ---------------------------------------------------------------------------
# Prediccion especifica de montana
# ---------------------------------------------------------------------------


async def montana_pasada(area: str, api_keys: Iterable[str]) -> list:
    """Prediccion de montana. Tiempo pasado.

    Args:
        area: Codigo de area de montana.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    if not area:
        raise ValueError("El parametro 'area' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion de montana pasada area=%s", area)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/especifica/montanna/pasada/area/{area}?api_key={{apiKey}}"
    )
    return await fetch_aemet_datos(endpoint_template, f"pred_montana_pasada_{area}", api_keys_list)


async def montana_pasada_dia(area: str, dia: str, api_keys: Iterable[str]) -> list:
    """Prediccion de montana para un dia especifico.

    Args:
        area: Codigo de area de montana.
        dia: Codigo de dia.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    if not area or not dia:
        raise ValueError("Los parametros 'area' y 'dia' son obligatorios.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion de montana area=%s dia=%s", area, dia)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/especifica/montanna/pasada/area/{area}/dia/{dia}?api_key={{apiKey}}"
    )
    return await fetch_aemet_datos(
        endpoint_template, f"pred_montana_pasada_{area}_{dia}", api_keys_list
    )


# ---------------------------------------------------------------------------
# Prediccion especifica: UVI y nivologica
# ---------------------------------------------------------------------------


async def uvi(dia: str, api_keys: Iterable[str]) -> list:
    """Prediccion de radiacion ultravioleta (UVI).

    Args:
        dia: Alcance de prediccion en dias (ej. '0', '1', '2').
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion UVI.
    """
    if not dia:
        raise ValueError("El parametro 'dia' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion UVI dia=%s", dia)

    endpoint_template = f"{BASE_URL}/api/prediccion/especifica/uvi/{dia}?api_key={{apiKey}}"
    return await fetch_aemet_datos(endpoint_template, f"pred_uvi_{dia}", api_keys_list)


async def nivologica(area: str, api_keys: Iterable[str]) -> list:
    """Prediccion nivologica (niveles de nieve) para un area.

    Args:
        area: Codigo de area nivologica.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion nivologica.
    """
    if not area:
        raise ValueError("El parametro 'area' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion nivologica area=%s", area)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/especifica/nivologica/{area}?api_key={{apiKey}}"
    )
    return await fetch_aemet_datos(endpoint_template, f"pred_nivologica_{area}", api_keys_list)


# ---------------------------------------------------------------------------
# Prediccion maritima
# ---------------------------------------------------------------------------


async def maritima_altamar(area: str, api_keys: Iterable[str]) -> list:
    """Prediccion maritima de alta mar.

    Args:
        area: Codigo de area maritima de alta mar.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    if not area:
        raise ValueError("El parametro 'area' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion maritima altamar area=%s", area)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/maritima/altamar/area/{area}?api_key={{apiKey}}"
    )
    return await fetch_aemet_datos(endpoint_template, f"pred_maritima_altamar_{area}", api_keys_list)


async def maritima_costera(costa: str, api_keys: Iterable[str]) -> list:
    """Prediccion maritima costera.

    Args:
        costa: Codigo de costa.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista con los datos de prediccion.
    """
    if not costa:
        raise ValueError("El parametro 'costa' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion maritima costera costa=%s", costa)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/maritima/costera/costa/{costa}?api_key={{apiKey}}"
    )
    return await fetch_aemet_datos(endpoint_template, f"pred_maritima_costera_{costa}", api_keys_list)


# ---------------------------------------------------------------------------
# Predicciones georreferenciadas
# ---------------------------------------------------------------------------


async def general_vectorial(api_keys: Iterable[str]) -> dict:
    """Prediccion general georreferenciada. Tiempo actual.

    Args:
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.
    """
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando prediccion general vectorial")

    endpoint_template = f"{BASE_URL}/api/prediccion/general/vectorial?api_key={{apiKey}}"
    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, "pred_general_vectorial", api_keys_list
    )


async def raster_ecmwf(area: str, api_keys: Iterable[str]) -> dict:
    """Modelo ECMWF georreferenciado.

    Args:
        area: Codigo de area ('atn', 'gbl').
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.
    """
    if not area:
        raise ValueError("El parametro 'area' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando ECMWF georreferenciado area=%s", area)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/modelos/raster/ecmwf/area/{area}?api_key={{apiKey}}"
    )
    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"pred_ecmwf_{area}", api_keys_list
    )


async def raster_harmonie(area: str, api_keys: Iterable[str]) -> dict:
    """Modelo Harmonie georreferenciado.

    Args:
        area: Codigo de area ('pnb', 'can').
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Respuesta de la API como diccionario.
    """
    if not area:
        raise ValueError("El parametro 'area' es obligatorio.")
    api_keys_list = validar_api_keys(api_keys)
    logger.info("Solicitando Harmonie georreferenciado area=%s", area)

    endpoint_template = (
        f"{BASE_URL}/api/prediccion/modelos/raster/harmonie/area/{area}?api_key={{apiKey}}"
    )
    return await fetch_con_reintentos_endpoint_aemet(
        endpoint_template, f"pred_harmonie_{area}", api_keys_list
    )
