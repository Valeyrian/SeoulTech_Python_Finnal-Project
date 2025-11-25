"""
Modèle de données Film pour l'application Netflux
"""


class Film:
    """
    Représente un film avec ses métadonnées
    
    Attributes:
        titre (str): Titre du film
        minute (int): Durée en minutes
        genres (list[str]): Liste des genres du film
        system_name (str): Identifiant système unique
        tiles (str): Chemin vers l'image miniature
        video (str): Chemin vers le fichier vidéo
    """
    
    def __init__(self, titre, minute, genres, system_name):
        """
        Initialise un film
        
        Args:
            titre (str): Titre du film
            minute (int|str): Durée en minutes
            genres (list[str]): Liste des genres
            system_name (str): Identifiant système unique
        """
        self.titre = titre
        self.minute = int(minute)
        self.genres = genres  # liste de chaînes
        self.system_name = system_name
        self.tiles = f"./data/movies_tiles/{system_name}.jpg"
        self.video = f"./data/movies/{system_name}.mp4"
    
    def __repr__(self):
        """Représentation textuelle du film"""
        return f"<Film titre='{self.titre}' ({self.minute} min)>"
    
    def __str__(self):
        """Chaîne de caractères pour l'affichage"""
        genres_str = ", ".join(self.genres)
        return f"{self.titre} ({self.minute}m) - {genres_str}"
    
    def __eq__(self, other):
        """Égalité basée sur le system_name"""
        if not isinstance(other, Film):
            return False
        return self.system_name == other.system_name
    
    def __hash__(self):
        """Hash basé sur le system_name pour utilisation dans sets/dicts"""
        return hash(self.system_name)
    
    def has_genre(self, genre):
        """
        Vérifie si le film appartient à un genre donné
        
        Args:
            genre (str): Genre à vérifier
            
        Returns:
            bool: True si le film a ce genre
        """
        return genre in self.genres
    
    def matches_keywords(self, keywords):
        """
        Vérifie si le titre correspond aux mots-clés
        
        Args:
            keywords (str): Mots-clés séparés par des espaces
            
        Returns:
            bool: True si au moins un mot-clé est trouvé
        """
        mots = keywords.lower().split()
        titre = self.titre.lower()
        return any(mot in titre for mot in mots)
