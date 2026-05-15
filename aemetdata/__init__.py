"""Paquete principal de aemetdata.

Proporciona acceso a todos los modulos de la API de AEMET OpenData.
"""

from .aemet_client import AemetClient
from . import antartida
from . import avisos
from . import climatologia
from . import imagenes
from . import incendios
from . import maestro
from . import mapas
from . import modelos
from . import observaciones
from . import prediccion
from . import redes
from . import utils

__all__ = [
    "AemetClient",
    "antartida",
    "avisos",
    "climatologia",
    "imagenes",
    "incendios",
    "maestro",
    "mapas",
    "modelos",
    "observaciones",
    "prediccion",
    "redes",
    "utils",
]

