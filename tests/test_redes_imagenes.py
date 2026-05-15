"""Tests del modulo redes e imagenes."""

from __future__ import annotations

import io
import tarfile

import pytest
from unittest.mock import patch, MagicMock

import aemetdata.redes as redes
import aemetdata.imagenes as imagenes
from tests.conftest import make_mock_client, json_response


def make_bytes_response(content: bytes) -> MagicMock:
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.content = content
    return resp


# ---------------------------------------------------------------------------
# Redes: radar
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_radar_nacional_ok():
    step1 = json_response({"estado": 200, "datos": "https://example.com/radar.gif"})
    step2 = make_bytes_response(b"GIF89a")
    client = make_mock_client([step1, step2])
    with patch("httpx.AsyncClient", return_value=client):
        result = await redes.radar_nacional(["clave1"])
    assert isinstance(result, bytes)
    assert result == b"GIF89a"


@pytest.mark.asyncio
async def test_radar_nacional_sin_url():
    """Si la respuesta no tiene URL de datos, retorna bytes vacios."""
    step1 = json_response({"estado": 200})
    client = make_mock_client([step1])
    with patch("httpx.AsyncClient", return_value=client):
        result = await redes.radar_nacional(["clave1"])
    assert result == b""


@pytest.mark.asyncio
async def test_radar_regional_ok():
    step1 = json_response({"estado": 200, "datos": "https://example.com/radar.gif"})
    step2 = make_bytes_response(b"\xff\xd8\xff")
    client = make_mock_client([step1, step2])
    with patch("httpx.AsyncClient", return_value=client):
        result = await redes.radar_regional("CAT", ["clave1"])
    assert isinstance(result, bytes)


@pytest.mark.asyncio
async def test_radar_regional_sin_producto():
    with pytest.raises(ValueError, match="obligatorio"):
        await redes.radar_regional("", ["clave1"])


# ---------------------------------------------------------------------------
# Redes: rayos
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_rayos_mapa_ok():
    resp = json_response({"estado": 200, "datos": "https://example.com/rayos.gif"})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await redes.rayos_mapa(["clave1"])
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# Redes: contaminacion, ozono, radiacion
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_contaminacion_fondo_ok():
    resp = json_response({"estado": 200})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await redes.contaminacion_fondo("CBA", "BEN", ["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_contaminacion_fondo_sin_params():
    with pytest.raises(ValueError, match="obligatorios"):
        await redes.contaminacion_fondo("", "BEN", ["clave1"])


@pytest.mark.asyncio
async def test_ozono_ok():
    resp = json_response({"estado": 200})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await redes.ozono("EL", ["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_ozono_sin_estacion():
    with pytest.raises(ValueError, match="obligatorio"):
        await redes.ozono("", ["clave1"])


@pytest.mark.asyncio
async def test_perfil_ozono_ok():
    resp = json_response({"estado": 200})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await redes.perfil_ozono("EL", ["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_radiacion_ok():
    resp = json_response({"estado": 200})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await redes.radiacion("SEV", "GHI", ["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_radiacion_sin_params():
    with pytest.raises(ValueError, match="obligatorios"):
        await redes.radiacion("", "GHI", ["clave1"])


# ---------------------------------------------------------------------------
# Imagenes: satelite NDVI y SST
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_imagenes_ndvi_ok():
    step1 = json_response({"estado": 200, "datos": "https://example.com/ndvi.png"})
    step2 = make_bytes_response(b"\x89PNG")
    client = make_mock_client([step1, step2])
    with patch("httpx.AsyncClient", return_value=client):
        result = await imagenes.satelite_ndvi(["clave1"])
    assert isinstance(result, bytes)
    assert result == b"\x89PNG"


@pytest.mark.asyncio
async def test_imagenes_sst_ok():
    step1 = json_response({"estado": 200, "datos": "https://example.com/sst.png"})
    step2 = make_bytes_response(b"\x89PNG")
    client = make_mock_client([step1, step2])
    with patch("httpx.AsyncClient", return_value=client):
        result = await imagenes.satelite_sst(["clave1"])
    assert isinstance(result, bytes)


@pytest.mark.asyncio
async def test_imagenes_ndvi_sin_url():
    """Si la respuesta no tiene URL de datos, retorna bytes vacios."""
    step1 = json_response({"estado": 200})
    client = make_mock_client([step1])
    with patch("httpx.AsyncClient", return_value=client):
        result = await imagenes.satelite_ndvi(["clave1"])
    assert result == b""
