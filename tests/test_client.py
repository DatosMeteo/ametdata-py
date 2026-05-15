"""Tests del AemetClient y del paquete principal."""

from __future__ import annotations

import pytest
from unittest.mock import patch

from aemetdata import AemetClient
from tests.conftest import make_mock_client, aemet_two_step, json_response


def test_client_inicializa_con_una_clave():
    client = AemetClient(api_keys="mi_clave")
    assert client.api_keys == ["mi_clave"]


def test_client_inicializa_con_lista():
    client = AemetClient(api_keys=["clave1", "clave2"])
    assert client.api_keys == ["clave1", "clave2"]


def test_client_sin_claves():
    with pytest.raises(ValueError):
        AemetClient(api_keys=[])


@pytest.mark.asyncio
async def test_client_observaciones_todas():
    http_client = make_mock_client(aemet_two_step([{"idema": "3195"}]))
    aemet = AemetClient(api_keys=["clave1"])
    with patch("httpx.AsyncClient", return_value=http_client):
        result = await aemet.observaciones_todas()
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_client_observaciones_estacion():
    http_client = make_mock_client(aemet_two_step([{"idema": "3195"}]))
    aemet = AemetClient(api_keys=["clave1"])
    with patch("httpx.AsyncClient", return_value=http_client):
        result = await aemet.observaciones_estacion("3195")
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_client_prediccion_municipio_diaria():
    http_client = make_mock_client(aemet_two_step([{"municipio": "28079"}]))
    aemet = AemetClient(api_keys=["clave1"])
    with patch("httpx.AsyncClient", return_value=http_client):
        result = await aemet.prediccion_municipio_diaria("28079")
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_client_prediccion_municipio_horaria():
    http_client = make_mock_client(aemet_two_step([{"municipio": "28079"}]))
    aemet = AemetClient(api_keys=["clave1"])
    with patch("httpx.AsyncClient", return_value=http_client):
        result = await aemet.prediccion_municipio_horaria("28079")
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_client_municipios():
    http_client = make_mock_client(aemet_two_step([{"nombre": "Madrid"}]))
    aemet = AemetClient(api_keys=["clave1"])
    with patch("httpx.AsyncClient", return_value=http_client):
        result = await aemet.municipios()
    assert isinstance(result, list)


def test_import_todos_modulos():
    """Todos los submodulos deben ser importables sin error."""
    import aemetdata
    assert hasattr(aemetdata, "antartida")
    assert hasattr(aemetdata, "avisos")
    assert hasattr(aemetdata, "climatologia")
    assert hasattr(aemetdata, "imagenes")
    assert hasattr(aemetdata, "incendios")
    assert hasattr(aemetdata, "maestro")
    assert hasattr(aemetdata, "mapas")
    assert hasattr(aemetdata, "modelos")
    assert hasattr(aemetdata, "observaciones")
    assert hasattr(aemetdata, "prediccion")
    assert hasattr(aemetdata, "redes")
    assert hasattr(aemetdata, "utils")
