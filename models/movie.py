"""
Movie data model for the Netflux application.
"""


class Movie:
    """
    Represents a movie with its metadata.
    
    Attributes:
        title (str): Movie title
        minutes (int): Duration in minutes
        genres (list[str]): List of movie genres
        system_name (str): Unique system identifier
        tile_path (str): Path to the thumbnail image
        video_path (str): Path to the video file
    """
    
    def __init__(self, title, minutes, genres, system_name):
        """
        Initialize a movie.
        
        Args:
            title (str): Movie title
            minutes (int|str): Duration in minutes
            genres (list[str]): List of genres
            system_name (str): Unique system identifier
        """
        self.title = title
        self.minutes = int(minutes)
        self.genres = genres
        self.system_name = system_name
        self.tile_path = f"./data/movies_tiles/{system_name}.jpg"
        self.video_path = f"./data/movies/{system_name}.mp4"
        
    
    def __repr__(self):
        """Text representation of the movie."""
        return f"<Movie title='{self.title}' ({self.minutes} min)>"
    
    def __str__(self):
        """String representation for display."""
        genres_str = ", ".join(self.genres)
        return f"{self.title} ({self.minutes}m) - {genres_str}"
    
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
        Check if the title matches the keywords.
        
        Args:
            keywords (str): Keywords separated by spaces
            
        Returns:
            bool: True if at least one keyword is found
        """
        words = keywords.lower().split()
        title_lower = self.title.lower()
        return any(word in title_lower for word in words)


