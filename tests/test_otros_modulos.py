"""Tests de los modulos antartida, incendios, maestro, mapas y modelos."""

from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock

import aemetdata.antartida as antartida
import aemetdata.incendios as incendios
import aemetdata.maestro as maestro
import aemetdata.mapas as mapas
import aemetdata.modelos as modelos
from aemetdata.utils.suport_functions import AemetError
from tests.conftest import make_mock_client, aemet_two_step, json_response


# ---------------------------------------------------------------------------
# Antartida
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_antartida_datos_ok():
    client = make_mock_client(aemet_two_step([{"estacion": "ANT_01", "ta": -5.0}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await antartida.datos_antartida(
            "2024-01-01T00:00:00UTC",
            "2024-01-31T23:59:59UTC",
            "89064",
            ["clave1"],
        )
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_antartida_datos_sin_fechas():
    with pytest.raises(ValueError, match="obligatorios"):
        await antartida.datos_antartida("", "2024-01-31T23:59:59UTC", "89064", ["clave1"])


@pytest.mark.asyncio
async def test_antartida_datos_multiples_estaciones():
    """Dos estaciones retornan datos combinados."""
    client = make_mock_client(
        aemet_two_step([{"estacion": "89064"}]) + aemet_two_step([{"estacion": "89001"}])
    )
    with patch("httpx.AsyncClient", return_value=client):
        result = await antartida.datos_antartida(
            "2024-01-01T00:00:00UTC",
            "2024-01-31T23:59:59UTC",
            ["89064", "89001"],
            ["clave1"],
        )
    assert len(result) == 2


# ---------------------------------------------------------------------------
# Incendios
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_incendios_mapa_estimado_ok():
    resp = json_response({"estado": 200, "datos": "https://example.com/img.png"})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await incendios.mapa_riesgo_estimado("p", ["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_incendios_mapa_estimado_area_invalida():
    with pytest.raises(ValueError, match="Area"):
        await incendios.mapa_riesgo_estimado("x", ["clave1"])


@pytest.mark.asyncio
async def test_incendios_mapa_previsto_ok():
    resp = json_response({"estado": 200})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await incendios.mapa_riesgo_previsto("1", "p", ["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_incendios_mapa_previsto_dia_invalido():
    with pytest.raises(ValueError, match="dia"):
        await incendios.mapa_riesgo_previsto("5", "p", ["clave1"])


@pytest.mark.asyncio
async def test_incendios_riesgo_raster_ok():
    resp = json_response({"estado": 200})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await incendios.riesgo_raster(["clave1"])
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# Maestro
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_maestro_todos_municipios_ok():
    client = make_mock_client(aemet_two_step([{"id": "id28079", "nombre": "Madrid"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await maestro.todos_municipios(["clave1"])
    assert isinstance(result, list)
    assert result[0]["nombre"] == "Madrid"


@pytest.mark.asyncio
async def test_maestro_municipio_ok():
    client = make_mock_client(aemet_two_step([{"id": "id28079", "nombre": "Madrid"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await maestro.municipio("id28079", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_maestro_municipio_sin_codigo():
    with pytest.raises(ValueError, match="obligatorio"):
        await maestro.municipio("", ["clave1"])


@pytest.mark.asyncio
async def test_maestro_municipio_nombre_ok():
    client = make_mock_client(aemet_two_step([{"id": "id28079", "nombre": "Madrid"}]))
    with patch("httpx.AsyncClient", return_value=client):
        result = await maestro.municipio_por_nombre("Madrid", ["clave1"])
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_maestro_municipio_nombre_vacio():
    with pytest.raises(ValueError, match="obligatorio"):
        await maestro.municipio_por_nombre("", ["clave1"])


# ---------------------------------------------------------------------------
# Mapas
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_mapas_analisis_ok():
    resp = json_response({"estado": 200, "datos": "https://example.com/img.jpg"})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await mapas.analisis_ultimo(["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_mapas_significativos_ok():
    resp = json_response({"estado": 200})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await mapas.mapas_significativos("2024-01-01", "nacional", "0-12", ["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_mapas_significativos_ambito_invalido():
    with pytest.raises(ValueError, match="ambito"):
        await mapas.mapas_significativos("2024-01-01", "invalido", "0-12", ["clave1"])


@pytest.mark.asyncio
async def test_mapas_previstos_ok():
    resp = json_response({"estado": 200})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await mapas.mapas_previstos("12", ["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_mapas_previstos_sin_alcance():
    with pytest.raises(ValueError, match="obligatorio"):
        await mapas.mapas_previstos("", ["clave1"])


# ---------------------------------------------------------------------------
# Modelos
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_modelos_aespol_ok():
    resp = json_response({"estado": 200, "datos": "https://example.com/modelo.grib"})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await modelos.aespol("00", "12", "hs", ["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_modelos_aespol_sin_parametros():
    with pytest.raises(ValueError, match="obligatorios"):
        await modelos.aespol("", "12", "hs", ["clave1"])


@pytest.mark.asyncio
async def test_modelos_aewam_ok():
    resp = json_response({"estado": 200})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await modelos.aewam("00", "24", "shts", ["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_modelos_harmonie_peninsula_ok():
    resp = json_response({"estado": 200})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await modelos.harmonie_peninsula("00", "24", "33", "grib", ["clave1"])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_modelos_harmonie_peninsula_formato_invalido():
    with pytest.raises(ValueError, match="formato"):
        await modelos.harmonie_peninsula("00", "24", "33", "xml", ["clave1"])


@pytest.mark.asyncio
async def test_modelos_harmonie_canarias_ok():
    resp = json_response({"estado": 200})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await modelos.harmonie_canarias("12", "48", "11", "netcdf", ["clave1"])
    assert isinstance(result, dict)
