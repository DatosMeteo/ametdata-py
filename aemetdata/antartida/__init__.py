"""Modulo de datos de la Antartida de AEMET."""

from __future__ import annotations

import logging
from typing import Iterable

from ..utils.suport_functions import (
    fetch_aemet_datos,
    procesar_lista_ids,
    validar_api_keys,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://opendata.aemet.es/opendata"


async def datos_antartida(
    fecha_inicio: str,
    fecha_fin: str,
    identificacion: str | Iterable[str],
    api_keys: Iterable[str],
) -> list:
    """Descarga datos de observacion de la Antartida en un rango de fechas.

    Args:
        fecha_inicio: Fecha inicial en formato AAAA-MM-DDTHH:MM:SSUTC.
        fecha_fin: Fecha final en formato AAAA-MM-DDTHH:MM:SSUTC.
        identificacion: Identificador de estacion o lista de identificadores.
        api_keys: Iterable con las claves API de AEMET.

    Returns:
        Lista de observaciones.

    Raises:
        ValueError: Si los parametros no son validos.
        AemetError: Si hay error descargando los datos.
    """
    if not fecha_inicio or not fecha_fin:
        raise ValueError("Los parametros 'fecha_inicio' y 'fecha_fin' son obligatorios.")

    ids = procesar_lista_ids(identificacion, "identificacion")
    api_keys_list = validar_api_keys(api_keys)

    all_results: list = []
    for id_item in ids:
        logger.info(
            "Solicitando datos Antartida para estacion %s entre %s y %s",
            id_item, fecha_inicio, fecha_fin,
        )
        endpoint_template = (
            f"{BASE_URL}/api/antartida/datos/fechaini/{fecha_inicio}"
            f"/fechafin/{fecha_fin}/estacion/{id_item}?api_key={{apiKey}}"
        )
        datos = await fetch_aemet_datos(
            endpoint_template, f"antartida_{id_item}_{fecha_inicio[:10]}_{fecha_fin[:10]}", api_keys_list
        )
        all_results.extend(datos)

    return all_results
