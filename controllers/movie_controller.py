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
        Search for movies by title and director.
        
        Args:
            query (str): Search text (keywords)
        
        Returns:
            list: Movies matching the search, or all movies if query is empty
        """
        self._current_search = query.strip()
        
        if not self._current_search:
            return self.get_all_movies()
        
        # Use method that searches in both title and director
        return self.catalog.get_movies_by_title_or_director(self._current_search)
    
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
    
    def get_movie_count(self):
        """
        Return the total number of movies in the catalog.
        
        Returns:
            int: Total number of movies
        """
        return len(self.catalog.movies)

    def _get_favorite_directors(self, user):
        """
        Extract unique directors from user's favorite movies.
        
        Args:
            user: User instance containing favorite movies
        
        Returns:
            set: Set of director names from favorite movies
        """
        favorite_directors = set()
        
        if not hasattr(user, 'favorites') or not user.favorites:
            return favorite_directors
        
        for movie_id in user.favorites:
            movie = self.catalog.get_movie_by_system_name(movie_id)
            if movie and hasattr(movie, 'director') and movie.director:
                directors = [d.strip() for d in movie.director.split(',')]
                favorite_directors.update(directors)
        
        return favorite_directors

    def get_recommended_movies(self, user):
        """
        Return a list of recommended movies based on the user's preferred genres and favorite directors.
        Excludes movies already watched by the user.
        
        Args:
            user: User instance containing genre preferences, favorites, and watched list
        
        Returns:
            list: Movies matching the user's preferred genres and favorite directors,
                  excluding already watched movies
        """
        if not user:
            print("No user provided for recommendations.")
            return []
        
        if not hasattr(user, 'liked_genres') and not user.liked_genres and not hasattr(user, 'favorites') and not user.favorites :
            print("User has no liked genres and no favorites films so no recommendation posible")
            return []
        
        # Get movies based on liked genres
        recommended_movies = self.catalog.get_movies_from_multiple_genres(user.liked_genres)
        
        # Get directors from favorite movies using the helper function
        favorite_directors = self._get_favorite_directors(user)
        
        # Add movies from favorite directors
        if favorite_directors:
            all_movies = self.catalog.get_all_catalog()
            for movie in all_movies:
                if movie not in recommended_movies and hasattr(movie, 'director') and movie.director:
                    movie_directors = [d.strip() for d in movie.director.split(',')]
                    # Check if any director matches
                    if any(director in favorite_directors for director in movie_directors):
                        recommended_movies.append(movie)
        
        # Exclude watched movies
        if hasattr(user, 'watched') and user.watched:
            watched_set = set(user.watched)
            recommended_movies = [
                movie for movie in recommended_movies 
                if movie.system_name not in watched_set
            ]
        
        return recommended_movies
    
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
    
    def get_wathclist_movie(self, user):
        """
        Return a list of the user's watchlist movies.
        
        Args:
            user: User instance containing watchlist movies
        
        Returns:
            list: User's watchlist movies
        """
        if not user or not user.watchlist:
            return []
        
        watchlist_movies = []
        for movie_id in user.watchlist:
            movie = self.catalog.get_movie_by_system_name(movie_id)
            if movie:
                watchlist_movies.append(movie)
        
        return watchlist_movies

    def get_watched_movie(self, user):
        """
        Return a list of the user's watched movies.
        
        Args:
            user: User instance containing watched movies
        
        Returns:
            list: User's watched movies
        """
        if not user or not user.watched:
            return []
        
        watched_movies = []
        for movie_id in user.watched:
            movie = self.catalog.get_movie_by_system_name(movie_id)
            if movie:
                watched_movies.append(movie)
        
        return watched_movies




