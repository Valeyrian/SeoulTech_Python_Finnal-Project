"""
Catalog model for managing the movie collection.
"""
from .movie import Movie


class Catalog:
    """
    Manages the movie collection and provides search/filtering methods.
    
    Attributes:
        path (str): Path to the CSV file
        movies (list[Movie]): List of loaded movies
    """
    
    def __init__(self, path="./data/catalogue.csv"):
        """
        Initialize the catalog.
        
        Args:
            path (str): Path to the movies CSV file
        """
        self.path = path
        self.movies = []
    
    def load_from_csv(self):
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
                        print(f"Warning: Line skipped (invalid format): {line}")
                        continue

                    title, minutes, genres, system_name = parts
                    genre_list = [g.strip() for g in genres.split(",")]

                    movie = Movie(title, minutes, genre_list, system_name)
                    self.movies.append(movie)
                    
            print(f"Success: {len(self.movies)} movie(s) loaded from {self.path}")
        except FileNotFoundError:
            print(f"Error: File not found: {self.path}")
            raise
        except Exception as e:
            print(f"Error: Failed to load the catalog: {e}")
            raise
    
    def print_movies(self):
        """Display all movies in the console."""
        for movie in self.movies:
            print(movie)
    
    def get_movies_by_genre(self, genre):
        """
        Get all movies of a given genre.
        
        Args:
            genre (str): Genre to search for
            
        Returns:
            list[Movie]: List of matching movies
        """
        results = []
        for movie in self.movies:
            if genre in movie.genres:
                results.append(movie)
        return results
    
    def get_movies_from_multiple_genres(self, genres_list):
        """
        Get movies belonging to at least one of the genres in the list.
        
        Args:
            genres_list (list[str]): List of genres to search for
            
        Returns:
            list[Movie]: Movies matching at least one genre
        """
        if not genres_list:
            return []
            
        results = []
        for movie in self.movies:
            if any(genre in movie.genres for genre in genres_list):
                results.append(movie)
        return results
    
    def get_movies_by_title(self, keywords):
        """
        Search for movies by keywords in the title.
        
        Args:
            keywords (str): Keywords separated by spaces
            
        Returns:
            list[Movie]: Movies whose title contains at least one keyword
        """
        if not keywords:
            return []
            
        words = keywords.lower().split()
        results = []

        for movie in self.movies:
            title_lower = movie.title.lower()
            if any(word in title_lower for word in words):
                results.append(movie)

        return results
    
    def get_movie_by_system_name(self, system_name):
        """
        Get a movie by its system identifier.
        
        Args:
            system_name (str): System identifier of the movie
            
        Returns:
            Movie|None: The found movie or None
        """
        for movie in self.movies:
            if movie.system_name == system_name:
                return movie
        return None
    
    def get_all_genres(self):
        """
        Get all unique genres from the catalog.
        
        Returns:
            list[str]: Sorted list of genres
        """
        genres = set()
        for movie in self.movies:
            for genre in movie.genres:
                genres.add(genre)
        return sorted(genres)
    
    def get_all_catalog(self):
        """
        Get all movies from the catalog.
        
        Returns:
            list[Movie]: Complete list of movies
        """
        return self.movies
    
    def get_movie_count(self):
        """
        Return the number of movies in the catalog.
        
        Returns:
            int: Number of movies
        """
        return len(self.movies)
    
    def __len__(self):
        """Allow using len(catalog)."""
        return len(self.movies)
    
    def __iter__(self):
        """Allow iterating over movies: for movie in catalog."""
        return iter(self.movies)
    
    def __repr__(self):
        """Text representation of the catalog."""
        return f"<Catalog path='{self.path}' movies={len(self.movies)}>"
