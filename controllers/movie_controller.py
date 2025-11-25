"""
MovieController - Controller for managing movie business logic.

Responsibilities:
    - Movie search and filtering
    - Application state management
    - Interface between the model (Catalogue) and the view (MainApp)
"""

class MovieController:
    """Controller for movie management."""
    
    def __init__(self, catalogue):
        """
        Initialize the controller with a catalogue.
        
        Args:
            catalogue: Catalogue instance containing the movies
        """
        self.catalogue = catalogue
        self._current_filter = None  # Active filter (None = all movies)
        self._current_search = ""    # Active search query
    
    def get_all_movies(self):
        """
        Return all movies from the catalogue.
        
        Returns:
            list: List of all Film objects
        """
        return self.catalogue.getAllCatalogue()
    
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
        
        return self.catalogue.getFilmsByTitle(self._current_search)
    
    def filter_by_genre(self, genre):
        """
        Filter movies by genre.
        
        Args:
            genre (str): Genre to filter (e.g., "Action", "Comedy")
        
        Returns:
            list: Movies of the specified genre
        """
        self._current_filter = genre
        return self.catalogue.getFilmsByGenre(genre)
    
    def get_available_genres(self):
        """
        Return the list of all available genres (without duplicates).
        
        Returns:
            list: Sorted list of unique genres
        """
        return list(self.catalogue.getAllTheGenres())
    
    def get_movies_grouped_by_genre(self, movie_list=None):
        """
        Return a dict {genre: [movies]} grouped by genre.
        
        Args:
            movie_list (list, optional): List of movies to group.
                                        If None, uses all movies from the catalogue.
        
        Returns:
            dict: Dictionary with genres as keys and lists of movies as values
        """
        # If no list provided, get all movies
        if movie_list is None:
            movie_list = self.get_all_movies()
        
        grouped = {}
        
        # Iterate through all movies in the list
        for film in movie_list:
            # For each genre of the movie
            for genre in film.genres:
                # Create the genre list if it doesn't exist
                if genre not in grouped:
                    grouped[genre] = []
                # Add the movie to this genre (avoid duplicates)
                if film not in grouped[genre]:
                    grouped[genre].append(film)
        
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
        """Return the total number of movies in the catalogue."""
        return len(self.catalogue.films)

    def get_recommanded_movies(self,user):
        """
        Return a list of recommended movies based on the user's preferred genres.
        
        Args:
            user: User instance containing genre preferences
        
        Returns:
            list: Movies matching the user's preferred genres
        """
        if not user or not user.likedGenre:
            return []
        
        return self.catalogue.getFilmsFromMultipleGenres(user.likedGenre)
    
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
            movie = self.catalogue.getFilmBySystemName(movie_id)
            if movie:
                favorite_movies.append(movie)
        
        return favorite_movies