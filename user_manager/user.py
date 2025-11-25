"""
Gestion des utilisateurs de l'application Netflux
Sauvegarde et chargement depuis un fichier JSON
"""
import json
import os
from typing import List, Dict, Optional


class User:
    """
    Classe représentant un utilisateur de l'application
    """
    
    def __init__(self, username: str, email: str = "", user_id: Optional[int] = None):
        """
        Initialise un utilisateur
        
        Args:
            username: Nom d'utilisateur
            email: Email de l'utilisateur
            user_id: ID unique de l'utilisateur (généré automatiquement si None)
        """
        self.user_id = user_id if user_id is not None else self._generate_id()
        self.username = username
        self.email = email
        self.favorites: List[str] = []  # Liste des codes films favoris
        self.watchlist: List[str] = []  # Liste des codes films à regarder
        self.watched: List[str] = []    # Liste des codes films déjà vus
        self.likedGenre: List[str] = []
        
    
    def _generate_id(self) -> int:
        """Génère un ID unique basé sur le timestamp"""
        import time
        return int(time.time() * 1000)
    
    # ========== GESTION DES FAVORIS ==========
    
    def add_favorite(self, film_code: str) -> bool:
        """
        Ajoute un film aux favoris
        
        Args:
            film_code: Code système du film
            
        Returns:
            True si ajouté, False si déjà présent
        """
        if film_code not in self.favorites:
            self.favorites.append(film_code)
            return True
        return False
    
    def remove_favorite(self, film_code: str) -> bool:
        """
        Retire un film des favoris
        
        Args:
            film_code: Code système du film
            
        Returns:
            True si retiré, False si non présent
        """
        if film_code in self.favorites:
            self.favorites.remove(film_code)
            return True
        return False
    
    def is_favorite(self, film_code: str) -> bool:
        """Vérifie si un film est dans les favoris"""
        return film_code in self.favorites
    
    def get_favorite(self) -> List[str]:
        """Retourne la liste des films favoris"""
        return self.favorites
    
    # ========== GESTION DE LA WATCHLIST ==========
    
    def add_to_watchlist(self, film_code: str) -> bool:
        """Ajoute un film à la liste de lecture"""
        if film_code not in self.watchlist:
            self.watchlist.append(film_code)
            return True
        return False
    
    def remove_from_watchlist(self, film_code: str) -> bool:
        """Retire un film de la liste de lecture"""
        if film_code in self.watchlist:
            self.watchlist.remove(film_code)
            return True
        return False
    
    def is_in_watchlist(self, film_code: str) -> bool:
        """Vérifie si un film est dans la watchlist"""
        return film_code in self.watchlist
    
    def get_watchlist(self) -> List[str]:
        """Retourne la liste des films dans la watchlist"""
        return self.watchlist
    # ========== GESTION DE L'HISTORIQUE ==========
    
    def mark_as_watched(self, film_code: str) -> bool:
        """Marque un film comme vu"""
        if film_code not in self.watched:
            self.watched.append(film_code)
            # Retirer de la watchlist si présent
            self.remove_from_watchlist(film_code)
            return True
        return False
    
    def is_watched(self, film_code: str) -> bool:
        """Vérifie si un film a été vu"""
        return film_code in self.watched
    
    def get_watched(self) -> List[str]:
        """Retourne la liste des films vus"""
        return self.watched
    # ========== Gestion des genres ==========

    def add_to_liked_genre(self, genre: str) -> bool:
        """Ajoute un genre a la liste de genre aimer"""
        if genre not in self.likedGenre :
            self.likedGenre.append(genre)
            return True
        
        return False
    
    def remove_a_liked_genre(self, genre: str) -> bool:
        if genre in self.likedGenre:
            self.likedGenre.remove(genre)
            return True
        return False
    
    def is_in_liked_genre(self, genre: str) -> bool:
        """Vérifie si un genre est dans la liste des genre aimer"""
        return genre in self.likedGenre
    
    def get_liked_genre(self) -> List[str]:
        """Retourne la liste des genre aimer"""
        return self.likedGenre
    
    # ========== SÉRIALISATION ==========
    
    def to_dict(self) -> Dict:
        """
        Convertit l'utilisateur en dictionnaire pour JSON
        
        Returns:
            Dictionnaire représentant l'utilisateur
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
        Crée un utilisateur depuis un dictionnaire
        
        Args:
            data: Dictionnaire contenant les données utilisateur
            
        Returns:
            Instance de User
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
    Gestionnaire pour sauvegarder et charger les utilisateurs
    """
    
    def __init__(self, data_file: str = "user_manager/users.json"):
        """
        Initialise le gestionnaire d'utilisateurs
        
        Args:
            data_file: Chemin du fichier JSON de sauvegarde
        """
        self.data_file = data_file
        self.users: Dict[int, User] = {}
        self.current_user: Optional[User] = None
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Crée le dossier data s'il n'existe pas"""
        directory = os.path.dirname(self.data_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    # ========== CHARGEMENT ET SAUVEGARDE ==========
    
    def load_users(self) -> bool:
        """
        Charge les utilisateurs depuis le fichier JSON
        
        Returns:
            True si chargement réussi, False sinon
        """
        if not os.path.exists(self.data_file):
            print(f"⚠️  Fichier {self.data_file} non trouvé, création d'une nouvelle base")
            return False
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.users = {}
            for user_data in data.get("users", []):
                user = User.from_dict(user_data)
                self.users[user.user_id] = user
            
            # Charger l'utilisateur actuel
            current_user_id = data.get("current_user_id")
            if current_user_id and current_user_id in self.users:
                self.current_user = self.users[current_user_id]
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des utilisateurs: {e}")
            return False
    
    def save_users(self) -> bool:
        """
        Sauvegarde les utilisateurs dans le fichier JSON
        
        Returns:
            True si sauvegarde réussie, False sinon
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
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    # ========== GESTION DES UTILISATEURS ==========
    
    def create_user(self, username: str, email: str = "") -> User:
        """
        Crée un nouvel utilisateur
        
        Args:
            username: Nom d'utilisateur
            email: Email de l'utilisateur
            
        Returns:
            L'utilisateur créé
        """
        user = User(username, email)
        self.users[user.user_id] = user
        self.current_user = user
        self.save_users()
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Récupère un utilisateur par son ID"""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Récupère un utilisateur par son nom"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def set_current_user(self, user: User) -> None:
        """Définit l'utilisateur actuel"""
        if user.user_id in self.users:
            self.current_user = user
            self.save_users()
    
    def delete_user(self, user_id: int) -> bool:
        """Supprime un utilisateur"""
        if user_id in self.users:
            user = self.users[user_id]
            del self.users[user_id]
            if self.current_user and self.current_user.user_id == user_id:
                self.current_user = None
            self.save_users()
            return True
        return False
    
    def get_all_users(self) -> List[User]:
        """Retourne la liste de tous les utilisateurs"""
        return list(self.users.values())
    
    # ========== MÉTHODES PRATIQUES ==========
    
    def get_or_create_default_user(self) -> User:
        """
        Récupère ou crée un utilisateur par défaut
        Utile pour démarrer rapidement l'application
        
        Returns:
            Utilisateur par défaut
        """
        if self.current_user:
            return self.current_user
        
        # Chercher un utilisateur existant
        if self.users:
            self.current_user = list(self.users.values())[0]
            return self.current_user
        
        # Créer un utilisateur par défaut
        return self.create_user("User", "user@netflux.com")
