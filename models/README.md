# Models Package

Ce package contient les modèles de données de l'application Netflux.

## Structure

```
models/
├── __init__.py      # Exports Film et Catalogue
├── film.py          # Modèle Film
├── catalogue.py     # Modèle Catalogue
└── README.md        # Ce fichier
```

## Utilisation

### Import des modèles

```python
from models import Film, Catalogue

# Ou imports individuels
from models.film import Film
from models.catalogue import Catalogue
```

### Classe Film

Représente un film individuel avec ses métadonnées.

**Attributs :**
- `titre` (str) : Titre du film
- `minute` (int) : Durée en minutes
- `genres` (list[str]) : Liste des genres
- `system_name` (str) : Identifiant système unique
- `tiles` (str) : Chemin vers l'image miniature
- `video` (str) : Chemin vers le fichier vidéo

**Méthodes principales :**
- `has_genre(genre)` : Vérifie si le film appartient à un genre
- `matches_keywords(keywords)` : Vérifie si le titre correspond aux mots-clés

**Exemple :**
```python
film = Film("Pirates Des Caraïbes", 120, ["Action", "Aventure"], "pirates_des_caraibes")
print(film.titre)  # "Pirates Des Caraïbes"
print(film.has_genre("Action"))  # True
```

### Classe Catalogue

Gère la collection de films et fournit des méthodes de recherche/filtrage.

**Attributs :**
- `path` (str) : Chemin vers le fichier CSV
- `films` (list[Film]) : Liste des films chargés

**Méthodes principales :**
- `loadFromCSV()` : Charge les films depuis le CSV
- `getFilmsByGenre(genre)` : Récupère les films d'un genre
- `getFilmsFromMultipleGenres(genres_list)` : Récupère les films de plusieurs genres
- `getFilmsByTitle(keywords)` : Recherche par mots-clés dans le titre
- `getFilmBySystemName(system_name)` : Récupère un film par son ID
- `getAllTheGenres()` : Liste tous les genres uniques
- `getAllCatalogue()` : Retourne tous les films

**Exemple :**
```python
catalogue = Catalogue("./data/catalogue.csv")
catalogue.loadFromCSV()

# Recherche par genre
action_films = catalogue.getFilmsByGenre("Action")

# Recherche par titre
films = catalogue.getFilmsByTitle("pirates")

# Tous les genres
genres = catalogue.getAllTheGenres()
```

## Format CSV

Le fichier `catalogue.csv` doit respecter ce format :

```
titre:minute:genres:system_name
```

**Exemple :**
```
Pirates Des Caraïbes:120:Action,Aventure:pirates_des_caraibes
Inception:148:Science-Fiction,Action:inception
```

## Améliorations apportées

✅ **Séparation claire** : Les modèles sont isolés de la logique métier  
✅ **Méthodes magiques** : `__repr__`, `__str__`, `__eq__`, `__hash__`, `__len__`, `__iter__`  
✅ **Méthodes utilitaires** : `has_genre()`, `matches_keywords()`  
✅ **Documentation** : Docstrings complètes sur toutes les classes et méthodes  
✅ **Gestion d'erreurs** : Messages informatifs lors du chargement  
✅ **Type hints implicites** : Documentation claire des types attendus
