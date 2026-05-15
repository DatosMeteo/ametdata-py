"""Tests del modulo climatologia."""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, patch

import aemetdata.climatologia as clima
from aemetdata.utils.suport_functions import AemetError
from tests.conftest import make_mock_client, aemet_two_step


# ---------------------------------------------------------------------------
# Inventario
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_inventario_estaciones_ok():
    client = make_mock_client(aemet_two_step([{"indicativo": "3195"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await clima.inventario_estaciones(["clave1"])
    assert isinstance(result, list)
    assert result[0]["indicativo"] == "3195"


@pytest.mark.asyncio
async def test_inventario_estaciones_por_id_ok():
    client = make_mock_client(aemet_two_step([{"indicativo": "3195"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await clima.inventario_estaciones_por_id("3195", ["clave1"])
    assert isinstance(result, list)


# ---------------------------------------------------------------------------
# Datos mensuales
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_datos_mensuales_ok():
    """Datos mensuales para un anio (sin chunking)."""
    client = make_mock_client(aemet_two_step([{"mes": "2023-01", "tm_mes": 10.1}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await clima.datos_mensuales("3195", 2023, 2023, ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_datos_mensuales_sin_clave():
    with pytest.raises(ValueError):
        await clima.datos_mensuales("3195", 2023, 2023, [])


# ---------------------------------------------------------------------------
# Datos diarios
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_datos_diarios_ok():
    client = make_mock_client(aemet_two_step([{"fecha": "2024-01-01", "tmed": 12.5}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await clima.datos_diarios("3195", "2024-01-01", "2024-01-31", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_datos_diarios_todas_estaciones_ok():
    client = make_mock_client(aemet_two_step([{"fecha": "2024-01-01"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await clima.datos_diarios_todas_estaciones("2024-01-01", "2024-01-31", ["clave1"])
    assert isinstance(result, list)


# ---------------------------------------------------------------------------
# Datos horarios
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_datos_horarios_ok():
    client = make_mock_client(aemet_two_step([{"fecha": "2024-01-01T00:00:00", "ta": 10.0}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await clima.datos_horarios("3195", "2024-01-01T00:00:00UTC", "2024-01-02T00:00:00UTC", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_datos_horarios_todas_ok():
    client = make_mock_client(aemet_two_step([{"fecha": "2024-01-01T00:00:00"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await clima.datos_horarios_todas_estaciones(
            "2024-01-01T00:00:00UTC", "2024-01-02T00:00:00UTC", ["clave1"]
        )
    assert isinstance(result, list)


# ---------------------------------------------------------------------------
# Extremos y normales
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_datos_extremos_ok():
    client = make_mock_client(aemet_two_step([{"extremo": "datos"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await clima.datos_extremos("3195", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_datos_normales_ok():
    client = make_mock_client(aemet_two_step([{"normal": "datos"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await clima.datos_normales("3195", ["clave1"])
    assert isinstance(result, list)


# ---------------------------------------------------------------------------
# Rejillas y raster
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_rejillas_anuales_ok():
    client = make_mock_client(aemet_two_step([{"dato": "rejilla"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await clima.rejillas_anuales("p", "ta", "2023", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_rejillas_mensuales_ok():
    client = make_mock_client(aemet_two_step([{"dato": "rejilla"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await clima.rejillas_mensuales("p", "ta", "2023", "01", ["clave1"])
    assert isinstance(result, list)
