"""
Modèle Catalogue pour gérer la collection de films
"""
from .film import Film


class Catalogue:
    """
    Gère la collection de films et fournit des méthodes de recherche/filtrage
    
    Attributes:
        path (str): Chemin vers le fichier CSV
        films (list[Film]): Liste des films chargés
    """
    
    def __init__(self, path="./data/catalogue.csv"):
        """
        Initialise le catalogue
        
        Args:
            path (str): Chemin vers le fichier CSV des films
        """
        self.path = path
        self.films = []
    
    def loadFromCSV(self):
        """
        Charge les films depuis le fichier CSV
        Format attendu: titre:minute:genres:system_name
        Les genres sont séparés par des virgules
        
        Raises:
            FileNotFoundError: Si le fichier CSV n'existe pas
            ValueError: Si une ligne a un format invalide
        """
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for ligne in f:
                    ligne = ligne.strip()
                    if not ligne:
                        continue  # ignorer les lignes vides

                    parts = [p.strip() for p in ligne.split(":")]

                    if len(parts) != 4:
                        print(f"⚠️  Ligne ignorée (format invalide) : {ligne}")
                        continue

                    titre, minute, genres, system_name = parts
                    genre_list = [g.strip() for g in genres.split(",")]

                    film = Film(titre, minute, genre_list, system_name)
                    self.films.append(film)
                    
            print(f" {len(self.films)} film(s) chargé(s) depuis {self.path}")
        except FileNotFoundError:
            print(f" Fichier non trouvé : {self.path}")
            raise
        except Exception as e:
            print(f" Erreur lors du chargement du catalogue : {e}")
            raise
    
    def printFilms(self):
        """Affiche tous les films dans la console"""
        for film in self.films:
            print(film)
    
    def getFilmsByGenre(self, genre):
        """
        Récupère tous les films d'un genre donné
        
        Args:
            genre (str): Genre à rechercher
            
        Returns:
            list[Film]: Liste des films correspondants
        """
        results = []
        for film in self.films:
            if genre in film.genres:
                results.append(film)
        return results
    
    def getFilmsFromMultipleGenres(self, genres_list):
        """
        Récupère les films appartenant à au moins un des genres de la liste
        
        Args:
            genres_list (list[str]): Liste des genres recherchés
            
        Returns:
            list[Film]: Films correspondant à au moins un genre
        """
        if not genres_list:
            return []
            
        results = []
        for film in self.films:
            if any(genre in film.genres for genre in genres_list):
                results.append(film)
        return results
    
    def getFilmsByTitle(self, keywords):
        """
        Recherche des films par mots-clés dans le titre
        
        Args:
            keywords (str): Mots-clés séparés par des espaces
            
        Returns:
            list[Film]: Films dont le titre contient au moins un mot-clé
        """
        if not keywords:
            return []
            
        mots = keywords.lower().split()
        results = []

        for film in self.films:
            titre = film.titre.lower()
            if any(mot in titre for mot in mots):
                results.append(film)

        return results
    
    def getFilmBySystemName(self, system_name):
        """
        Récupère un film par son identifiant système
        
        Args:
            system_name (str): Identifiant système du film
            
        Returns:
            Film|None: Le film trouvé ou None
        """
        for film in self.films:
            if film.system_name == system_name:
                return film
        return None
    
    def getAllTheGenres(self):
        """
        Récupère tous les genres uniques du catalogue
        
        Returns:
            list[str]: Liste triée des genres
        """
        genres = set()
        for film in self.films:
            for genre in film.genres:
                genres.add(genre)
        return sorted(genres)
    
    def getAllCatalogue(self):
        """
        Récupère tous les films du catalogue
        
        Returns:
            list[Film]: Liste complète des films
        """
        return self.films
    
    def get_film_count(self):
        """
        Retourne le nombre de films dans le catalogue
        
        Returns:
            int: Nombre de films
        """
        return len(self.films)
    
    def __len__(self):
        """Permet d'utiliser len(catalogue)"""
        return len(self.films)
    
    def __iter__(self):
        """Permet d'itérer sur les films : for film in catalogue"""
        return iter(self.films)
    
    def __repr__(self):
        """Représentation textuelle du catalogue"""
        return f"<Catalogue path='{self.path}' films={len(self.films)}>"
