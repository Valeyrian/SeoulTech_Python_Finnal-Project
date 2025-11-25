"""
Models package for the Netflux application.
Contains data classes and models.
"""
from .movie import Movie, Film
from .catalog import Catalog, Catalogue

__all__ = ['Movie', 'Catalog', 'Film', 'Catalogue']
