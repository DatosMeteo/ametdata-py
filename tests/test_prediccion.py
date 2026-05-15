"""Tests del modulo prediccion."""

from __future__ import annotations

import pytest
from unittest.mock import patch

import aemetdata.prediccion as pred
from tests.conftest import make_mock_client, aemet_two_step


@pytest.mark.asyncio
async def test_nacional_hoy_ok():
    client = make_mock_client(aemet_two_step([{"prediccion": "nacional"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.nacional_hoy(["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_nacional_manana_ok():
    client = make_mock_client(aemet_two_step([{"prediccion": "manana"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.nacional_manana(["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_nacional_pasadomanana_ok():
    client = make_mock_client(aemet_two_step([{"prediccion": "pasadomanana"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.nacional_pasadomanana(["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_nacional_medioplazo_ok():
    client = make_mock_client(aemet_two_step([{"prediccion": "medioplazo"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.nacional_medioplazo(["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_nacional_tendencia_ok():
    client = make_mock_client(aemet_two_step([{"prediccion": "tendencia"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.nacional_tendencia(["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_ccaa_hoy_ok():
    client = make_mock_client(aemet_two_step([{"ccaa": "79"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.ccaa_hoy("79", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_ccaa_hoy_sin_codigo():
    with pytest.raises(ValueError, match="obligatorio"):
        await pred.ccaa_hoy("", ["clave1"])


@pytest.mark.asyncio
async def test_ccaa_manana_ok():
    client = make_mock_client(aemet_two_step([{"ccaa": "79"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.ccaa_manana("79", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_ccaa_pasadomanana_ok():
    client = make_mock_client(aemet_two_step([{"ccaa": "79"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.ccaa_pasadomanana("79", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_ccaa_medioplazo_ok():
    client = make_mock_client(aemet_two_step([{"ccaa": "79"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.ccaa_medioplazo("79", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_provincia_hoy_ok():
    client = make_mock_client(aemet_two_step([{"provincia": "28"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.provincia_hoy("28", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_provincia_hoy_sin_codigo():
    with pytest.raises(ValueError, match="obligatorio"):
        await pred.provincia_hoy("", ["clave1"])


@pytest.mark.asyncio
async def test_provincia_manana_ok():
    client = make_mock_client(aemet_two_step([{"provincia": "28"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.provincia_manana("28", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_municipio_diaria_ok():
    client = make_mock_client(aemet_two_step([{"municipio": "28079"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.municipio_diaria("28079", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_municipio_diaria_sin_codigo():
    with pytest.raises(ValueError, match="obligatorio"):
        await pred.municipio_diaria("", ["clave1"])


@pytest.mark.asyncio
async def test_municipio_horaria_ok():
    client = make_mock_client(aemet_two_step([{"municipio": "28079"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.municipio_horaria("28079", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_playa_ok():
    client = make_mock_client(aemet_two_step([{"playa": "020401001"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.playa("020401001", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_playa_sin_codigo():
    with pytest.raises(ValueError, match="obligatorio"):
        await pred.playa("", ["clave1"])


@pytest.mark.asyncio
async def test_uvi_ok():
    client = make_mock_client(aemet_two_step([{"uvi": 3}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.uvi("0", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_uvi_sin_dia():
    with pytest.raises(ValueError, match="obligatorio"):
        await pred.uvi("", ["clave1"])


@pytest.mark.asyncio
async def test_nivologica_ok():
    client = make_mock_client(aemet_two_step([{"nivel": 2}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.nivologica("pir", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_maritima_altamar_ok():
    client = make_mock_client(aemet_two_step([{"maritima": "altamar"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.maritima_altamar("101", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_maritima_costera_ok():
    client = make_mock_client(aemet_two_step([{"maritima": "costera"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await pred.maritima_costera("101", ["clave1"])
    assert isinstance(result, list)
