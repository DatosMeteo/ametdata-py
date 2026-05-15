"""Tests para los helpers del modulo utils/suport_functions."""

from __future__ import annotations

import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch

from aemetdata.utils.suport_functions import (
    AemetError,
    MAX_CICLOS,
    fetch_aemet_datos,
    fetch_bytes_url,
    fetch_con_reintentos_endpoint_aemet,
    fetch_json_url,
    normalizar_datos,
    procesar_lista_ids,
    validar_api_keys,
)


# ---------------------------------------------------------------------------
# validar_api_keys
# ---------------------------------------------------------------------------


def test_validar_api_keys_lista_normal():
    keys = validar_api_keys(["key1", "key2"])
    assert keys == ["key1", "key2"]


def test_validar_api_keys_generador():
    keys = validar_api_keys(k for k in ["k1", "k2"])
    assert keys == ["k1", "k2"]


def test_validar_api_keys_vacia():
    with pytest.raises(ValueError):
        validar_api_keys([])


# ---------------------------------------------------------------------------
# procesar_lista_ids
# ---------------------------------------------------------------------------


def test_procesar_lista_ids_str():
    result = procesar_lista_ids("3195")
    assert result == ["3195"]


def test_procesar_lista_ids_lista():
    result = procesar_lista_ids(["3195", "3196"])
    assert result == ["3195", "3196"]


def test_procesar_lista_ids_tupla():
    result = procesar_lista_ids(("3195",))
    assert result == ["3195"]


def test_procesar_lista_ids_invalido():
    with pytest.raises(ValueError):
        procesar_lista_ids(12345)


def test_procesar_lista_ids_vacia():
    with pytest.raises(ValueError):
        procesar_lista_ids([])


# ---------------------------------------------------------------------------
# normalizar_datos
# ---------------------------------------------------------------------------


def test_normalizar_datos_lista():
    data = [{"a": 1}, {"b": 2}]
    assert normalizar_datos(data) == data


def test_normalizar_datos_dict():
    data = {"a": 1}
    assert normalizar_datos(data) == [{"a": 1}]


def test_normalizar_datos_json_str_lista():
    import json
    data_str = json.dumps([{"x": 1}])
    assert normalizar_datos(data_str) == [{"x": 1}]


def test_normalizar_datos_json_str_dict():
    import json
    data_str = json.dumps({"x": 1})
    assert normalizar_datos(data_str) == [{"x": 1}]


def test_normalizar_datos_str_invalido():
    result = normalizar_datos("texto plano")
    assert isinstance(result, list)
    assert len(result) == 1


# ---------------------------------------------------------------------------
# fetch_json_url
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fetch_json_url_ok():
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = [{"key": "value"}]

    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_resp)

    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await fetch_json_url("https://example.com/data", "test")

    assert result == [{"key": "value"}]


@pytest.mark.asyncio
async def test_fetch_json_url_error():
    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=httpx.ConnectError("fail"))

    with patch("httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(AemetError):
            await fetch_json_url("https://example.com/data", "test")


# ---------------------------------------------------------------------------
# fetch_bytes_url
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fetch_bytes_url_ok():
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.content = b"\x89PNG"

    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_resp)

    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await fetch_bytes_url("https://example.com/img.png", "test")

    assert result == b"\x89PNG"


@pytest.mark.asyncio
async def test_fetch_bytes_url_error():
    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=httpx.ConnectError("fail"))

    with patch("httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(AemetError):
            await fetch_bytes_url("https://example.com/img.png", "test")


# ---------------------------------------------------------------------------
# fetch_con_reintentos_endpoint_aemet
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fetch_con_reintentos_exito_primera_clave():
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.headers = {"Content-Type": "application/json"}
    mock_resp.json.return_value = {"estado": 200, "datos": "https://example.com/data"}

    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_resp)

    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await fetch_con_reintentos_endpoint_aemet(
            "https://opendata.aemet.es/api/test?api_key={apiKey}",
            "test",
            ["clave1"],
        )

    assert result == {"estado": 200, "datos": "https://example.com/data"}


@pytest.mark.asyncio
async def test_fetch_con_reintentos_falla_todas():
    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
        "429", request=MagicMock(), response=MagicMock(status_code=429)
    )
    mock_client.get = AsyncMock(return_value=mock_resp)

    with patch("httpx.AsyncClient", return_value=mock_client):
        with patch("asyncio.sleep", AsyncMock()):
            with pytest.raises(AemetError):
                await fetch_con_reintentos_endpoint_aemet(
                    "https://opendata.aemet.es/api/test?api_key={apiKey}",
                    "test",
                    ["clave1"],
                )


@pytest.mark.asyncio
async def test_fetch_con_reintentos_segunda_clave():
    """La primera clave falla, la segunda debe tener exito."""
    ok_resp = MagicMock()
    ok_resp.raise_for_status = MagicMock()
    ok_resp.headers = {"Content-Type": "application/json"}
    ok_resp.json.return_value = {"estado": 200}

    fail_resp = MagicMock()
    fail_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
        "429", request=MagicMock(), response=MagicMock(status_code=429)
    )

    call_count = 0

    async def mock_get(url, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return fail_resp
        return ok_resp

    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = mock_get

    with patch("httpx.AsyncClient", return_value=mock_client):
        with patch("asyncio.sleep", AsyncMock()):
            result = await fetch_con_reintentos_endpoint_aemet(
                "https://opendata.aemet.es/api/test?api_key={apiKey}",
                "test",
                ["clave_mala", "clave_buena"],
            )

    assert result == {"estado": 200}


# ---------------------------------------------------------------------------
# fetch_aemet_datos
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fetch_aemet_datos_ok():
    resp1 = MagicMock()
    resp1.raise_for_status = MagicMock()
    resp1.headers = {"Content-Type": "application/json"}
    resp1.json.return_value = {"estado": 200, "datos": "https://example.com/data.json"}

    resp2 = MagicMock()
    resp2.raise_for_status = MagicMock()
    resp2.json.return_value = [{"campo": "valor"}]

    call_count = 0

    async def mock_get(url, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return resp1
        return resp2

    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = mock_get

    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await fetch_aemet_datos(
            "https://opendata.aemet.es/api/test?api_key={apiKey}",
            "test",
            ["clave1"],
        )

    assert result == [{"campo": "valor"}]


@pytest.mark.asyncio
async def test_fetch_aemet_datos_estado_error():
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.headers = {"Content-Type": "application/json"}
    resp.json.return_value = {"estado": 404, "descripcion": "No encontrado"}

    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=resp)

    with patch("httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(AemetError, match="404"):
            await fetch_aemet_datos(
                "https://opendata.aemet.es/api/test?api_key={apiKey}",
                "test",
                ["clave1"],
            )
