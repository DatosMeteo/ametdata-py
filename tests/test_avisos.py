"""Tests del modulo avisos."""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

import aemetdata.avisos as avisos
from tests.conftest import make_mock_client


def bytes_response(content: bytes) -> MagicMock:
    """Respuesta mock que devuelve bytes."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.headers = {"Content-Type": "application/json"}
    resp.json.return_value = {"estado": 200, "datos": "https://example.com/data.tar.gz"}
    return resp


def tar_gz_response(content: bytes) -> MagicMock:
    """Respuesta mock binaria."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.content = content
    return resp


@pytest.mark.asyncio
async def test_avisos_cap_ultimo_area_ok():
    """Debe llamar al endpoint y descargar el tar.gz."""
    import io
    import tarfile

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        data = b"<alert>contenido</alert>"
        info = tarfile.TarInfo(name="aviso.cap")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    tar_content = buf.getvalue()

    step1_resp = MagicMock()
    step1_resp.raise_for_status = MagicMock()
    step1_resp.headers = {"Content-Type": "application/json"}
    step1_resp.json.return_value = {"estado": 200, "datos": "https://example.com/data.tar.gz"}

    step2_resp = MagicMock()
    step2_resp.raise_for_status = MagicMock()
    step2_resp.content = tar_content

    client = make_mock_client([step1_resp, step2_resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await avisos.avisos_cap_ultimo_area("61", ["clave1"])

    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_avisos_cap_ultimo_area_invalido():
    with pytest.raises(ValueError, match="area"):
        await avisos.avisos_cap_ultimo_area("INVALIDO", ["clave1"])


@pytest.mark.asyncio
async def test_avisos_vectorial_ultimo_ok():
    from tests.conftest import json_response
    resp = json_response({"estado": 200, "datos": "https://example.com/aviso.zip"})
    client = make_mock_client([resp])
    with patch("httpx.AsyncClient", return_value=client):
        result = await avisos.avisos_vectorial_ultimo(["clave1"])
    assert isinstance(result, dict)
    assert "datos" in result or "estado" in result
