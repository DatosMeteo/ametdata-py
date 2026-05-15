"""Cliente de alto nivel para la API de AEMET OpenData.

Proporciona un punto de entrada unificado para acceder a todos los modulos.
"""

from __future__ import annotations

import logging
from typing import Iterable

from .utils.suport_functions import validar_api_keys

logger = logging.getLogger(__name__)


class AemetClient:
    """Cliente de alto nivel para AEMET OpenData.

    Permite acceder a todos los modulos de la API usando la misma instancia,
    gestionando la rotacion de claves API de forma transparente.

    Attributes:
        api_keys: Lista de claves API para acceder a AEMET.

    Example::

        import asyncio
        from aemetdata import AemetClient

        client = AemetClient(api_keys=["mi_clave_aemet"])
        datos = asyncio.run(client.observaciones.todas())
    """

    def __init__(self, api_keys: str | Iterable[str]) -> None:
        """Inicializa el cliente con una o varias claves API.

        Args:
            api_keys: Clave API (str) o lista de claves API de AEMET.

        Raises:
            ValueError: Si no se proporciona ninguna clave API.
        """
        if isinstance(api_keys, str):
            api_keys = [api_keys]
        self.api_keys: list[str] = validar_api_keys(api_keys)
        logger.debug("AemetClient inicializado con %d clave(s) API.", len(self.api_keys))

        # Modulos disponibles como atributos del cliente
        self._setup_modules()

    def _setup_modules(self) -> None:
        """Configura accesos a los modulos del paquete."""
        # Se importan aqui para evitar importaciones circulares y permitir
        # que el cliente sea usado de forma stateless o stateful.
        from . import (
            antartida,
            avisos,
            climatologia,
            imagenes,
            incendios,
            maestro,
            mapas,
            modelos,
            observaciones,
            prediccion,
            redes,
        )

        self._antartida = antartida
        self._avisos = avisos
        self._climatologia = climatologia
        self._imagenes = imagenes
        self._incendios = incendios
        self._maestro = maestro
        self._mapas = mapas
        self._modelos = modelos
        self._observaciones = observaciones
        self._prediccion = prediccion
        self._redes = redes

    # ------------------------------------------------------------------
    # Metodos de conveniencia para los modulos mas comunes
    # ------------------------------------------------------------------

    async def observaciones_todas(self) -> list:
        """Datos de observacion de todas las estaciones (ultimas 24h)."""
        return await self._observaciones.todas(self.api_keys)

    async def observaciones_estacion(self, idema: str) -> list:
        """Datos de observacion de una estacion especifica."""
        return await self._observaciones.datos_estacion(idema, self.api_keys)

    async def prediccion_municipio_diaria(self, municipio: str) -> list:
        """Prediccion diaria para un municipio (codigo municipio)."""
        return await self._prediccion.municipio_diaria(municipio, self.api_keys)

    async def prediccion_municipio_horaria(self, municipio: str) -> list:
        """Prediccion horaria para un municipio (codigo municipio)."""
        return await self._prediccion.municipio_horaria(municipio, self.api_keys)

    async def municipios(self) -> list:
        """Lista de todos los municipios."""
        return await self._maestro.todos_municipios(self.api_keys)

