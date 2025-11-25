"""
MovieController - Controller for managing movie business logic.

Responsibilities:
    - Movie search and filtering
    - Application state management
    - Interface between the model (Catalog) and the view (MainApp)
"""

class MovieController:
    """
    Controller for movie management.
    
    Handles business logic for movie operations including searching, filtering,
    and organizing movies for display.
    
    Attributes:
        catalog: Catalog instance containing the movies
        _current_filter (str): Active filter (None = all movies)
        _current_search (str): Active search query
    """
    
    def __init__(self, catalog):
        """
        Initialize the controller with a catalog.
        
        Args:
            catalog: Catalog instance containing the movies
        """
        self.catalog = catalog
        self._current_filter = None
        self._current_search = ""
    
    def get_all_movies(self):
        """
        Return all movies from the catalog.
        
        Returns:
            list: List of all Movie objects
        """
        return self.catalog.get_all_catalog()
    
    def search_movies(self, query):
        """
        Search for movies by title.
        
        Args:
            query (str): Search text (keywords)
        
        Returns:
            list: Movies matching the search, or all movies if query is empty
        """
        self._current_search = query.strip()
        
        if not self._current_search:
            return self.get_all_movies()
        
        return self.catalog.get_movies_by_title(self._current_search)
    
    def filter_by_genre(self, genre):
        """
        Filter movies by genre.
        
        Args:
            genre (str): Genre to filter (e.g., "Action", "Comedy")
        
        Returns:
            list: Movies of the specified genre
        """
        self._current_filter = genre
        return self.catalog.get_movies_by_genre(genre)
    
    def get_available_genres(self):
        """
        Return the list of all available genres (without duplicates).
        
        Returns:
            list: Sorted list of unique genres
        """
        return list(self.catalog.get_all_genres())
    
    def get_movies_grouped_by_genre(self, movie_list=None):
        """
        Return a dict {genre: [movies]} grouped by genre.
        
        Args:
            movie_list (list, optional): List of movies to group.
                                        If None, uses all movies from the catalog.
        
        Returns:
            dict: Dictionary with genres as keys and lists of movies as values
        """
        if movie_list is None:
            movie_list = self.get_all_movies()
        
        grouped = {}
        
        for movie in movie_list:
            for genre in movie.genres:
                if genre not in grouped:
                    grouped[genre] = []
                if movie not in grouped[genre]:
                    grouped[genre].append(movie)
        
        return grouped
    
    def get_current_view(self):
        """
        Return the movies to display based on the active filter/search.
        
        Returns:
            list: Movies matching the current state
        """
        if self._current_search:
            return self.search_movies(self._current_search)
        elif self._current_filter:
            return self.filter_by_genre(self._current_filter)
        else:
            return self.get_all_movies()
    
    def reset_filters(self):
        """Reset all filters and searches."""
        self._current_filter = None
        self._current_search = ""
        return self.get_all_movies()
    
    def get_movie_count(self):
        """
        Return the total number of movies in the catalog.
        
        Returns:
            int: Total number of movies
        """
        return len(self.catalog.movies)

    def get_recommanded_movies(self, user):
        """
        Return a list of recommended movies based on the user's preferred genres.
        
        Args:
            user: User instance containing genre preferences
        
        Returns:
            list: Movies matching the user's preferred genres
        """
        if not user or not hasattr(user, 'liked_genres'):
            if user and hasattr(user, 'likedGenre'):
                liked_genres = user.likedGenre
            else:
                return []
        else:
            liked_genres = user.liked_genres
            
        if not liked_genres:
            return []
        
        return self.catalog.get_movies_from_multiple_genres(liked_genres)
    
    def get_favorite_movies(self, user):
        """
        Return a list of the user's favorite movies.
        
        Args:
            user: User instance containing favorite movies
        
        Returns:
            list: User's favorite movies
        """
        if not user or not user.favorites:
            return []
        
        favorite_movies = []
        for movie_id in user.favorites:
            movie = self.catalog.get_movie_by_system_name(movie_id)
            if movie:
                favorite_movies.append(movie)
        
        return favorite_movies
    
    # Legacy method names for backwards compatibility
    get_recommended_movies = get_recommanded_movies