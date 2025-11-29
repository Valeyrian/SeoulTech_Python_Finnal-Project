"""
Movie data model for the Netflux application.
"""


class Movie:
    """
    Represents a movie with its metadata.
    
    Attributes:
        title (str): Movie title
        year (int): Release year
        minutes (int): Duration in minutes
        genres (list[str]): List of movie genres
        system_name (str): Unique system identifier
        director (str): Director name(s)
        cast (str): Main cast members
        synopsis (str): Movie synopsis/description
        tile_path (str): Path to the thumbnail image
        video_path (str): Path to the video file (trailer)
    """
    
    def __init__(self, title, year, minutes, genres, system_name, director="", cast="", synopsis=""):
        """
        Initialize a movie.
        
        Args:
            title (str): Movie title
            year (int|str): Release year
            minutes (int|str): Duration in minutes
            genres (list[str]): List of genres
            system_name (str): Unique system identifier
            director (str, optional): Director name(s)
            cast (str, optional): Main cast members
            synopsis (str, optional): Movie synopsis
        """
        self.title = title
        self.year = int(year) if year else 0
        self.minutes = int(minutes)
        self.genres = genres
        self.system_name = system_name
        self.director = director
        self.cast = cast
        self.synopsis = synopsis
        self.tile_path = f"./data/movies_tiles/{system_name}.jpg"
        self.video_path = f"./data/movies/{system_name}.mp4"     
    
    def __repr__(self):
        """Text representation of the movie."""
        return f"<Movie title='{self.title}' ({self.year}) - {self.minutes} min>"
    
    def __str__(self):
        """String representation for display."""
        genres_str = ", ".join(self.genres)
        return f"{self.title} ({self.year}) - {self.minutes}m - {genres_str}"
    
    def __eq__(self, other):
        """Equality based on system_name."""
        if not isinstance(other, Movie):
            return False
        return self.system_name == other.system_name
    
    def __hash__(self):
        """Hash based on system_name for use in sets/dicts."""
        return hash(self.system_name)
    
    def has_genre(self, genre):
        """
        Check if the movie belongs to a given genre.
        
        Args:
            genre (str): Genre to check
            
        Returns:
            bool: True if the movie has this genre
        """
        return genre in self.genres
    
    def matches_keywords(self, keywords):
        """
        Check if the movie matches the search keywords.
        Searches in title, synopsis, director, and cast.
        
        Args:
            keywords (str): Keywords separated by spaces
            
        Returns:
            bool: True if at least one keyword is found
        """
        if not keywords:
            return False
            
        words = keywords.lower().split()
        title_lower = self.title.lower()
        synopsis_lower = self.synopsis.lower() if self.synopsis else ""
        director_lower = self.director.lower() if self.director else ""
        cast_lower = self.cast.lower() if self.cast else ""
        
        # Search in all fields
        for word in words:
            if (word in title_lower or 
                word in synopsis_lower or 
                word in director_lower or 
                word in cast_lower):
                return True
        
        return False


