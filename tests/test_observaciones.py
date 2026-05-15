"""Tests del modulo observaciones."""

from __future__ import annotations

import pytest
from unittest.mock import patch

import aemetdata.observaciones as obs
from aemetdata.utils.suport_functions import AemetError
from tests.conftest import make_mock_client, aemet_two_step


@pytest.mark.asyncio
async def test_todas_ok():
    client = make_mock_client(aemet_two_step([{"idema": "3195", "ta": 20.5}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await obs.todas(["clave1"])
    assert isinstance(result, list)
    assert result[0]["idema"] == "3195"


@pytest.mark.asyncio
async def test_todas_sin_claves():
    with pytest.raises(ValueError):
        await obs.todas([])


@pytest.mark.asyncio
async def test_datos_estacion_ok():
    client = make_mock_client(aemet_two_step([{"idema": "3195", "ta": 20.5}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await obs.datos_estacion("3195", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_datos_estacion_lista():
    """Multiples estaciones deben retornar datos combinados."""
    client = make_mock_client(
        aemet_two_step([{"idema": "3195"}]) + aemet_two_step([{"idema": "3196"}])
    )
    with patch("httpx.AsyncClient", return_value=client):
        result = await obs.datos_estacion(["3195", "3196"], ["clave1"])
    assert len(result) == 2


@pytest.mark.asyncio
async def test_diezminutal_todas_ok():
    client = make_mock_client(aemet_two_step([{"idema": "3195"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await obs.diezminutal_todas(["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_diezminutal_estacion_ok():
    client = make_mock_client(aemet_two_step([{"idema": "3195"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await obs.diezminutal_estacion("3195", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_diezminutal_fecha_estacion_ok():
    client = make_mock_client(aemet_two_step([{"idema": "3195"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await obs.diezminutal_fecha_estacion("2024-01-01", "3195", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_diezminutal_fecha_estacion_sin_fecha():
    with pytest.raises(ValueError, match="obligatorio"):
        await obs.diezminutal_fecha_estacion("", "3195", ["clave1"])


@pytest.mark.asyncio
async def test_diezminutal_ccaa_ok():
    client = make_mock_client(aemet_two_step([{"idema": "3195"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await obs.diezminutal_ccaa("83", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_diezminutal_ccaa_sin_codigo():
    with pytest.raises(ValueError, match="obligatorio"):
        await obs.diezminutal_ccaa("", ["clave1"])


@pytest.mark.asyncio
async def test_mensajes_tipo_ok():
    client = make_mock_client(aemet_two_step([{"mensaje": "SYNOP datos"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await obs.mensajes_tipo("SYNOP", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_mensajes_tipo_sin_tipo():
    with pytest.raises(ValueError, match="obligatorio"):
        await obs.mensajes_tipo("", ["clave1"])
