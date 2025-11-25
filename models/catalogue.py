"""
Catalogue model for managing the movie collection.
"""
from .film import Film


class Catalogue:
    """
    Manages the movie collection and provides search/filtering methods.
    
    Attributes:
        path (str): Path to the CSV file
        films (list[Film]): List of loaded movies
    """
    
    def __init__(self, path="./data/catalogue.csv"):
        """
        Initialize the catalogue.
        
        Args:
            path (str): Path to the movies CSV file
        """
        self.path = path
        self.films = []
    
    def loadFromCSV(self):
        """
        Load movies from the CSV file.
        Expected format: title:minutes:genres:system_name
        Genres are separated by commas.
        
        Raises:
            FileNotFoundError: If the CSV file does not exist
            ValueError: If a line has an invalid format
        """
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines

                    parts = [p.strip() for p in line.split(":")]

                    if len(parts) != 4:
                        print(f"⚠️  Line skipped (invalid format): {line}")
                        continue

                    titre, minute, genres, system_name = parts
                    genre_list = [g.strip() for g in genres.split(",")]

                    film = Film(titre, minute, genre_list, system_name)
                    self.films.append(film)
                    
            print(f" {len(self.films)} movie(s) loaded from {self.path}")
        except FileNotFoundError:
            print(f" File not found: {self.path}")
            raise
        except Exception as e:
            print(f" Error loading the catalogue: {e}")
            raise
    
    def printFilms(self):
        """Display all movies in the console."""
        for film in self.films:
            print(film)
    
    def getFilmsByGenre(self, genre):
        """
        Get all movies of a given genre.
        
        Args:
            genre (str): Genre to search for
            
        Returns:
            list[Film]: List of matching movies
        """
        results = []
        for film in self.films:
            if genre in film.genres:
                results.append(film)
        return results
    
    def getFilmsFromMultipleGenres(self, genres_list):
        """
        Get movies belonging to at least one of the genres in the list.
        
        Args:
            genres_list (list[str]): List of genres to search for
            
        Returns:
            list[Film]: Movies matching at least one genre
        """
        if not genres_list:
            return []
            
        results = []
        for film in self.films:
            if any(genre in film.genres for genre in genres_list):
                results.append(film)
        return results
    
    def getFilmsByTitle(self, keywords):
        """
        Search for movies by keywords in the title.
        
        Args:
            keywords (str): Keywords separated by spaces
            
        Returns:
            list[Film]: Movies whose title contains at least one keyword
        """
        if not keywords:
            return []
            
        words = keywords.lower().split()
        results = []

        for film in self.films:
            title = film.titre.lower()
            if any(word in title for word in words):
                results.append(film)

        return results
    
    def getFilmBySystemName(self, system_name):
        """
        Get a movie by its system identifier.
        
        Args:
            system_name (str): System identifier of the movie
            
        Returns:
            Film|None: The found movie or None
        """
        for film in self.films:
            if film.system_name == system_name:
                return film
        return None
    
    def getAllTheGenres(self):
        """
        Get all unique genres from the catalogue.
        
        Returns:
            list[str]: Sorted list of genres
        """
        genres = set()
        for film in self.films:
            for genre in film.genres:
                genres.add(genre)
        return sorted(genres)
    
    def getAllCatalogue(self):
        """
        Get all movies from the catalogue.
        
        Returns:
            list[Film]: Complete list of movies
        """
        return self.films
    
    def get_film_count(self):
        """
        Return the number of movies in the catalogue.
        
        Returns:
            int: Number of movies
        """
        return len(self.films)
    
    def __len__(self):
        """Allow using len(catalogue)."""
        return len(self.films)
    
    def __iter__(self):
        """Allow iterating over movies: for film in catalogue."""
        return iter(self.films)
    
    def __repr__(self):
        """Text representation of the catalogue."""
        return f"<Catalogue path='{self.path}' films={len(self.films)}>"
