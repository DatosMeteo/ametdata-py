"""Utilidades internas del paquete aemetdata."""

from .suport_functions import (
    AemetError,
    MAX_CICLOS,
    descargar_archivo_tar_gz,
    fetch_aemet_datos,
    fetch_bytes_url,
    fetch_con_reintentos_endpoint_aemet,
    fetch_json_url,
    get_relativedelta,
    normalizar_datos,
    procesar_lista_ids,
    validar_api_keys,
)

__all__ = [
    "AemetError",
    "MAX_CICLOS",
    "descargar_archivo_tar_gz",
    "fetch_aemet_datos",
    "fetch_bytes_url",
    "fetch_con_reintentos_endpoint_aemet",
    "fetch_json_url",
    "get_relativedelta",
    "normalizar_datos",
    "procesar_lista_ids",
    "validar_api_keys",
]
