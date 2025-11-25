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
        self.favorites: List[str] = []  # List of favorite movie codes
        self.watchlist: List[str] = []  # List of movies to watch
        self.watched: List[str] = []    # List of already watched movies
        self.likedGenre: List[str] = []
        
    
    def _generate_id(self) -> int:
        """Generate a unique ID based on timestamp."""
        import time
        return int(time.time() * 1000)
    
    # ========== FAVORITES MANAGEMENT ==========
    
    def add_favorite(self, film_code: str) -> bool:
        """
        Add a movie to favorites.
        
        Args:
            film_code: System code of the movie
            
        Returns:
            True if added, False if already present
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
            True if removed, False if not present
        """
        if film_code in self.favorites:
            self.favorites.remove(film_code)
            return True
        return False
    
    def is_favorite(self, film_code: str) -> bool:
        """Check if a movie is in favorites."""
        return film_code in self.favorites
    
    def get_favorite(self) -> List[str]:
        """Return the list of favorite movies."""
        return self.favorites
    
    # ========== WATCHLIST MANAGEMENT ==========
    
    def add_to_watchlist(self, film_code: str) -> bool:
        """Add a movie to the watchlist."""
        if film_code not in self.watchlist:
            self.watchlist.append(film_code)
            return True
        return False
    
    def remove_from_watchlist(self, film_code: str) -> bool:
        """Remove a movie from the watchlist."""
        if film_code in self.watchlist:
            self.watchlist.remove(film_code)
            return True
        return False
    
    def is_in_watchlist(self, film_code: str) -> bool:
        """Check if a movie is in the watchlist."""
        return film_code in self.watchlist
    
    def get_watchlist(self) -> List[str]:
        """Return the list of movies in the watchlist."""
        return self.watchlist
    
    # ========== HISTORY MANAGEMENT ==========
    
    def mark_as_watched(self, film_code: str) -> bool:
        """Mark a movie as watched."""
        if film_code not in self.watched:
            self.watched.append(film_code)
            # Remove from watchlist if present
            self.remove_from_watchlist(film_code)
            return True
        return False
    
    def is_watched(self, film_code: str) -> bool:
        """Check if a movie has been watched."""
        return film_code in self.watched
    
    def get_watched(self) -> List[str]:
        """Return the list of watched movies."""
        return self.watched
    
    # ========== GENRE MANAGEMENT ==========

    def add_to_liked_genre(self, genre: str) -> bool:
        """Add a genre to the liked genres list."""
        if genre not in self.likedGenre :
            self.likedGenre.append(genre)
            return True
        
        return False
    
    def remove_a_liked_genre(self, genre: str) -> bool:
        """Remove a genre from the liked genres list."""
        if genre in self.likedGenre:
            self.likedGenre.remove(genre)
            return True
        return False
    
    def is_in_liked_genre(self, genre: str) -> bool:
        """Check if a genre is in the liked genres list."""
        return genre in self.likedGenre
    
    def get_liked_genre(self) -> List[str]:
        """Return the list of liked genres."""
        return self.likedGenre
    
    # ========== SERIALIZATION ==========
    
    def to_dict(self) -> Dict:
        """
        Convert the user to a dictionary for JSON.
        
        Returns:
            Dictionary representing the user
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "favorites": self.favorites,
            "watchlist": self.watchlist,
            "watched": self.watched,
            "likedGenres": self.likedGenre
            
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """
        Create a user from a dictionary.
        
        Args:
            data: Dictionary containing user data
            
        Returns:
            User instance
        """
        user = cls(
            username=data["username"],
            user_id=data.get("user_id")
        )
        user.favorites = data.get("favorites", [])
        user.watchlist = data.get("watchlist", [])
        user.watched = data.get("watched", [])
        user.likedGenre = data.get("likedGenres", [])
        return user
    
    def __repr__(self):
        return f"<User {self.username} (ID: {self.user_id})>"


class UserManager:
    """
    Manager for saving and loading users.
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
    
    # ========== LOADING AND SAVING ==========
    
    def load_users(self) -> bool:
        """
        Load users from the JSON file.
        
        Returns:
            True if loading successful, False otherwise
        """
        if not os.path.exists(self.data_file):
            print(f"⚠️  File {self.data_file} not found, creating a new database")
            return False
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.users = {}
            for user_data in data.get("users", []):
                user = User.from_dict(user_data)
                self.users[user.user_id] = user
            
            # Load current user
            current_user_id = data.get("current_user_id")
            if current_user_id and current_user_id in self.users:
                self.current_user = self.users[current_user_id]
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading users: {e}")
            return False
    
    def save_users(self) -> bool:
        """
        Save users to the JSON file.
        
        Returns:
            True if saving successful, False otherwise
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
            print(f"❌ Error saving: {e}")
            return False
    
    # ========== USER MANAGEMENT ==========
    
    def create_user(self, username: str, email: str = "") -> User:
        """
        Create a new user.
        
        Args:
            username: Username
            email: User's email
            
        Returns:
            The created user
        """
        user = User(username, email)
        self.users[user.user_id] = user
        self.current_user = user
        self.save_users()
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by their ID."""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by their username."""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def set_current_user(self, user: User) -> None:
        """Set the current user."""
        if user.user_id in self.users:
            self.current_user = user
            self.save_users()
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        if user_id in self.users:
            user = self.users[user_id]
            del self.users[user_id]
            if self.current_user and self.current_user.user_id == user_id:
                self.current_user = None
            self.save_users()
            return True
        return False
    
    def get_all_users(self) -> List[User]:
        """Return the list of all users."""
        return list(self.users.values())
    
    # ========== UTILITY METHODS ==========
    
    def get_or_create_default_user(self) -> User:
        """
        Get or create a default user.
        Useful for quickly starting the application.
        
        Returns:
            Default user
        """
        if self.current_user:
            return self.current_user
        
        # Look for an existing user
        if self.users:
            self.current_user = list(self.users.values())[0]
            return self.current_user
        
        # Create a default user
        return self.create_user("User", "user@netflux.com")
