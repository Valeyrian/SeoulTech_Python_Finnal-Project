"""
MovieController - Contrôleur pour gérer la logique métier des films
Responsabilités :
- Recherche et filtrage des films
- Gestion des états de l'application
- Interface entre le modèle (Catalogue) et la vue (MainApp)
"""

class MovieController:
    """Contrôleur pour la gestion des films"""
    
    def __init__(self, catalogue):
        """
        Initialise le contrôleur avec un catalogue
        
        Args:
            catalogue: Instance de Catalogue contenant les films
        """
        self.catalogue = catalogue
        self._current_filter = None  # filtre actif (None = tous les films)
        self._current_search = ""    # recherche active
    
    def get_all_movies(self):
        """
        Retourne tous les films du catalogue
        
        Returns:
            list: Liste de tous les objets Film
        """
        return self.catalogue.getAllCatalogue()
    
    def search_movies(self, query):
        """
        Recherche des films par titre
        
        Args:
            query (str): Texte de recherche (mots-clés)
        
        Returns:
            list: Films correspondant à la recherche, ou tous les films si query vide
        """
        self._current_search = query.strip()
        
        if not self._current_search:
            return self.get_all_movies()
        
        return self.catalogue.getFilmsByTitle(self._current_search)
    
    def filter_by_genre(self, genre):
        """
        Filtre les films par genre
        
        Args:
            genre (str): Genre à filtrer (ex: "Action", "Comedie")
        
        Returns:
            list: Films du genre spécifié
        """
        self._current_filter = genre
        return self.catalogue.getFilmsByGenre(genre)
    
    def get_available_genres(self):
        """
        Retourne la liste de tous les genres disponibles (sans doublons)
        
        Returns:
            list: Liste des genres uniques triés
        """
        return list(self.catalogue.getAllTheGenres())
    
    def get_movies_grouped_by_genre(self, movie_list=None):
        """
        Retourne un dict {genre: [films]} groupé par genre
        
        Args:
            movie_list (list, optional): Liste de films à grouper.
                                        Si None, utilise tous les films du catalogue
        
        Returns:
            dict: Dictionnaire avec les genres en clés et listes de films en valeurs
        """
        # Si aucune liste fournie, prendre tous les films
        if movie_list is None:
            movie_list = self.get_all_movies()
        
        grouped = {}
        
        # Parcourir tous les films de la liste
        for film in movie_list:
            # Pour chaque genre du film
            for genre in film.genres:
                # Créer la liste du genre si elle n'existe pas
                if genre not in grouped:
                    grouped[genre] = []
                # Ajouter le film à ce genre (éviter les doublons)
                if film not in grouped[genre]:
                    grouped[genre].append(film)
        
        return grouped
    
    def get_current_view(self):
        """
        Retourne les films à afficher selon le filtre/recherche actif
        
        Returns:
            list: Films correspondant à l'état actuel
        """
        if self._current_search:
            return self.search_movies(self._current_search)
        elif self._current_filter:
            return self.filter_by_genre(self._current_filter)
        else:
            return self.get_all_movies()
    
    def reset_filters(self):
        """Réinitialise tous les filtres et recherches"""
        self._current_filter = None
        self._current_search = ""
        return self.get_all_movies()
    
    def get_movie_count(self):
        """Retourne le nombre total de films dans le catalogue"""
        return len(self.catalogue.films)

    def get_recommanded_movies(self,user):
        """
        Retourne une liste de films recommandés basée sur les genres préférés de l'utilisateur
        
        Args:
            user: Instance de User contenant les préférences de genres
        
        Returns:
            list: Films correspondant aux genres préférés de l'utilisateur
        """
        if not user or not user.likedGenre:
            return []
        
        return self.catalogue.getFilmsFromMultipleGenres(user.likedGenre)
    
    def get_favorite_movies(self, user):
        """
        Retourne une liste de films favoris de l'utilisateur
        
        Args:
            user: Instance de User contenant les films favoris
        
        Returns:
            list: Films favoris de l'utilisateur
        """
        if not user or not user.favorites:
            return []
        
        favorite_movies = []
        for movie_id in user.favorites:
            movie = self.catalogue.getFilmBySystemName(movie_id)
            if movie:
                favorite_movies.append(movie)
        
        return favorite_movies