"""
Models package for the Netflux application.
Contains data classes and models.
"""
from .movie import Movie
from .catalog import Catalog

__all__ = ['Movie', 'Catalog']