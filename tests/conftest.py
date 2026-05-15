"""Fixtures y helpers compartidos para los tests de aemetdata."""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock


def make_mock_client(side_effects: list):
    """Crea un mock de httpx.AsyncClient con respuestas configuradas.

    Args:
        side_effects: Lista de respuestas (MagicMock) en orden de llamada.

    Returns:
        Tupla (mock_client, lista_resps) lista para parchear httpx.AsyncClient.
    """
    call_index = 0
    results = list(side_effects)

    async def mock_get(url, **kwargs):
        nonlocal call_index
        resp = results[call_index % len(results)]
        call_index += 1
        if isinstance(resp, Exception):
            raise resp
        return resp

    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = mock_get
    return mock_client


def json_response(data: dict | list, status_code: int = 200) -> MagicMock:
    """Crea una respuesta mock con contenido JSON."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.status_code = status_code
    resp.headers = {"Content-Type": "application/json"}
    resp.json.return_value = data
    return resp


def aemet_two_step(data: list | dict, datos_url: str = "https://example.com/data.json"):
    """Devuelve la lista de dos respuestas del patron AEMET de dos pasos."""
    step1 = json_response({"estado": 200, "datos": datos_url})
    step2 = json_response(data)
    return [step1, step2]
