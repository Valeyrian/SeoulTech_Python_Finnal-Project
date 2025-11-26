"""
User management for the Netflux application.
Saving and loading from a JSON file.
"""
import json
import os
from typing import List, Dict, Optional


class User:
    """
    Class representing an application user.
    
    Attributes:
        user_id (int): Unique user identifier
        username (str): Username
        email (str): User's email address
        favorites (list[str]): List of favorite movie system names
        watchlist (list[str]): List of movies to watch
        watched (list[str]): List of watched movies
        liked_genres (list[str]): List of user's preferred genres
    """
    
    def __init__(self, username: str, email: str = "", user_id: Optional[int] = None):
        """
        Initialize a user.
        
        Args:
            username: Username
            email: User's email
            user_id: Unique user ID (auto-generated if None)
        """
        self.user_id = user_id if user_id is not None else self._generate_id()
        self.username = username
        self.email = email
        self.favorites: List[str] = []
        self.watchlist: List[str] = []
        self.watched: List[str] = []
        self.liked_genres: List[str] = []
        
    
    def _generate_id(self) -> int:
        """
        Generate a unique ID based on timestamp.
        
        Returns:
            int: Unique timestamp-based ID
        """
        import time
        return int(time.time() * 1000)
    
    def add_favorite(self, film_code: str) -> bool:
        """
        Add a movie to favorites.
        
        Args:
            film_code: System code of the movie
            
        Returns:
            bool: True if added, False if already present
        """
        if film_code not in self.favorites:
            self.favorites.append(film_code)
            return True
        return False
    
    def remove_favorite(self, film_code: str) -> bool:
        """
        Remove a movie from favorites.
        
        Args:
            film_code: System code of the movie
            
        Returns:
            bool: True if removed, False if not present
        """
        if film_code in self.favorites:
            self.favorites.remove(film_code)
            return True
        return False
    
    def is_favorite(self, film_code: str) -> bool:
        """
        Check if a movie is in favorites.
        
        Args:
            film_code: System code of the movie
            
        Returns:
            bool: True if in favorites
        """
        return film_code in self.favorites
    
    def get_favorite(self) -> List[str]:
        """
        Return the list of favorite movies.
        
        Returns:
            list[str]: List of favorite movie system names
        """
        return self.favorites
    
    def add_to_watchlist(self, film_code: str) -> bool:
        """
        Add a movie to the watchlist.
        
        Args:
            film_code: System code of the movie
            
        Returns:
            bool: True if added, False if already present
        """
        if film_code not in self.watchlist:
            self.watchlist.append(film_code)
            return True
        return False
    
    def remove_from_watchlist(self, film_code: str) -> bool:
        """
        Remove a movie from the watchlist.
        
        Args:
            film_code: System code of the movie
            
        Returns:
            bool: True if removed, False if not present
        """
        if film_code in self.watchlist:
            self.watchlist.remove(film_code)
            return True
        return False
    
    def is_in_watchlist(self, film_code: str) -> bool:
        """
        Check if a movie is in the watchlist.
        
        Args:
            film_code: System code of the movie
            
        Returns:
            bool: True if in watchlist
        """
        return film_code in self.watchlist
    
    def get_watchlist(self) -> List[str]:
        """
        Return the list of movies in the watchlist.
        
        Returns:
            list[str]: List of movie system names
        """
        return self.watchlist
    
    def mark_as_watched(self, film_code: str) -> bool:
        """
        Mark a movie as watched.
        
        Args:
            film_code: System code of the movie
            
        Returns:
            bool: True if marked, False if already watched
        """
        if film_code not in self.watched:
            self.watched.append(film_code)
            self.remove_from_watchlist(film_code)
            return True
        return False
    
    def unmark_as_watched(self, film_code: str) -> bool:
        """
        Unmark a movie as watched.
        
        Args:
            film_code: System code of the movie
        Returns:
            bool: True if unmarked, False if not present
        """
        if film_code in self.watched:
            self.watched.remove(film_code)
            return True
        return False


    def is_watched(self, film_code: str) -> bool:
        """
        Check if a movie has been watched.
        
        Args:
            film_code: System code of the movie
            
        Returns:
            bool: True if watched
        """
        return film_code in self.watched
    
    def get_watched(self) -> List[str]:
        """
        Return the list of watched movies.
        
        Returns:
            list[str]: List of movie system names
        """
        return self.watched
    
    def add_to_liked_genre(self, genre: str) -> bool:
        """
        Add a genre to the liked genres list.
        
        Args:
            genre: Genre name
            
        Returns:
            bool: True if added, False if already present
        """
        if genre not in self.liked_genres:
            self.liked_genres.append(genre)
            self.likedGenre = self.liked_genres
            return True
        return False
    
    def remove_a_liked_genre(self, genre: str) -> bool:
        """
        Remove a genre from the liked genres list.
        
        Args:
            genre: Genre name
            
        Returns:
            bool: True if removed, False if not present
        """
        if genre in self.liked_genres:
            self.liked_genres.remove(genre)
            self.likedGenre = self.liked_genres
            return True
        return False
    
    def is_in_liked_genre(self, genre: str) -> bool:
        """
        Check if a genre is in the liked genres list.
        
        Args:
            genre: Genre name
            
        Returns:
            bool: True if liked
        """
        return genre in self.liked_genres
    
    def get_liked_genre(self) -> List[str]:
        """
        Return the list of liked genres.
        
        Returns:
            list[str]: List of genre names
        """
        return self.liked_genres
    
    def to_dict(self) -> Dict:
        """
        Convert the user to a dictionary for JSON.
        
        Returns:
            dict: Dictionary representing the user
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "favorites": self.favorites,
            "watchlist": self.watchlist,
            "watched": self.watched,
            "likedGenres": self.liked_genres
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """
        Create a user from a dictionary.
        
        Args:
            data: Dictionary containing user data
            
        Returns:
            User: User instance
        """
        user = cls(
            username=data["username"],
            user_id=data.get("user_id")
        )
        user.favorites = data.get("favorites", [])
        user.watchlist = data.get("watchlist", [])
        user.watched = data.get("watched", [])
        user.liked_genres = data.get("likedGenres", [])
        user.likedGenre = user.liked_genres
        return user
    
    def __repr__(self):
        """String representation of the user."""
        return f"<User {self.username} (ID: {self.user_id})>"


class UserManager:
    """
    Manager for saving and loading users.
    
    Attributes:
        data_file (str): Path to the JSON save file
        users (dict): Dictionary of users by user_id
        current_user (User): Currently logged-in user
    """
    
    def __init__(self, data_file: str = "user_manager/users.json"):
        """
        Initialize the user manager.
        
        Args:
            data_file: Path to the JSON save file
        """
        self.data_file = data_file
        self.users: Dict[int, User] = {}
        self.current_user: Optional[User] = None
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Create the data folder if it doesn't exist."""
        directory = os.path.dirname(self.data_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def load_users(self) -> bool:
        """
        Load users from the JSON file.
        
        Returns:
            bool: True if loading successful, False otherwise
        """
        if not os.path.exists(self.data_file):
            print(f"Warning: File {self.data_file} not found, creating a new database")
            return False
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.users = {}
            for user_data in data.get("users", []):
                user = User.from_dict(user_data)
                self.users[user.user_id] = user
            
            current_user_id = data.get("current_user_id")
            if current_user_id and current_user_id in self.users:
                self.current_user = self.users[current_user_id]
            
            return True
            
        except Exception as e:
            print(f"Error: Failed to load users: {e}")
            return False
    
    def save_users(self) -> bool:
        """
        Save users to the JSON file.
        
        Returns:
            bool: True if saving successful, False otherwise
        """
        try:
            data = {
                "users": [user.to_dict() for user in self.users.values()],
                "current_user_id": self.current_user.user_id if self.current_user else None
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error: Failed to save users: {e}")
            return False
    
    def create_user(self, username: str, email: str = "") -> User:
        """
        Create a new user.
        
        Args:
            username: Username
            email: User's email
            
        Returns:
            User: The created user
        """
        user = User(username, email)
        self.users[user.user_id] = user
        self.current_user = user
        self.save_users()
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get a user by their ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User: User instance or None if not found
        """
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by their username.
        
        Args:
            username: Username to search for
            
        Returns:
            User: User instance or None if not found
        """
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def set_current_user(self, user: User) -> None:
        """
        Set the current user.
        
        Args:
            user: User instance to set as current
        """
        if user.user_id in self.users:
            self.current_user = user
            self.save_users()
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: User ID to delete
            
        Returns:
            bool: True if deleted successfully
        """
        if user_id in self.users:
            user = self.users[user_id]
            del self.users[user_id]
            if self.current_user and self.current_user.user_id == user_id:
                self.current_user = None
            self.save_users()
            return True
        return False
    
    def get_all_users(self) -> List[User]:
        """
        Return the list of all users.
        
        Returns:
            list[User]: List of all users
        """
        return list(self.users.values())
    
    def get_or_create_default_user(self) -> User:
        """
        Get or create a default user.
        Useful for quickly starting the application.
        
        Returns:
            User: Default user
        """
        if self.current_user:
            return self.current_user
        
        if self.users:
            self.current_user = list(self.users.values())[0]
            return self.current_user
        
        return self.create_user("User", "user@netflux.com")
