"""
Models package for the Netflux application.
Contains data classes and models.
"""
from .film import Movie, Film
from .catalogue import Catalog, Catalogue

__all__ = ['Movie', 'Catalog', 'Film', 'Catalogue']
