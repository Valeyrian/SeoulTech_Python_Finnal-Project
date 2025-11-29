import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap, QAction

from ui import Ui_MainWindow
from controllers import MovieController
from models import Catalog
from user_manager import UserManager
from user_manager.user_dialogs import show_login_dialog, confirm_logout, show_genre_preferences_dialog
from widgets.genre_row import GenreRow
from widgets.card import createFilmCard
from widgets.movie_detail_modal import MovieDetailModal

class MainApp(QMainWindow, Ui_MainWindow):
    """
    Main view of the Netflux application.
    
    Responsibilities:
        - UI display and user interactions
        - Does NOT contain business logic (delegated to the controller)
    """
    
    # ========== INITIALIZATION ==========
    
    def __init__(self, catalogue):
        """Initialize the main application window."""
        super().__init__()
        self.setupUi(self)  
        self.setWindowTitle("Netflux")
        self.setMinimumSize(1024, 768)
        
        # Load logo
        if not os.path.exists("./assets/logo.png"):
            pixmap = QPixmap("./assets/file_not_found.jpeg")
            raise FileNotFoundError("The file './assets/logo.png' is missing. Please make sure it exists.")
        else:
            pixmap = QPixmap("./assets/logo.png")
        self.logo.setPixmap(pixmap.scaled(140, 40))
        
        # Initialize managers and controllers
        self.user_manager = UserManager()
        self.user_manager.load_users()
        self.catalogue = catalogue
        self.controller = MovieController(catalogue)
        
        # View state
        self.current_view = "home"
        self.current_view_mode = "genre"
        self.displayed_cards = []
        
        # Initialize display
        self.show_movies()
        
        # Connect UI events
        self._connect_ui_events()
        self.setup_account_menu()
    
    def _connect_ui_events(self):
        """Connect all UI event handlers."""
        self.searchButton.clicked.connect(self.on_search_clicked)
        self.searchBar.returnPressed.connect(self.on_search_clicked)
        self.acceuilButton.clicked.connect(self.on_home_clicked)
        self.recomandationButton.clicked.connect(self.on_recomendation_clicked)
    
    # ========== UI SETUP METHODS ==========
    
    def setup_account_menu(self):
        """
        Configure the dropdown menu for the Account button.
        Displays Login or Logout depending on the connection status.
        """
        account_menu = QMenu(self)
        account_menu.setObjectName("accountMenu")
        
        if self.user_manager.current_user:
            user = self.user_manager.current_user
            
            # Username (disabled)
            profile_action = QAction(f"{user.username}", self)
            profile_action.setEnabled(False)
            account_menu.addAction(profile_action)
            
            account_menu.addSeparator()
            
            # Favorites
            favorites_action = QAction("My likes", self)
            favorites_action.triggered.connect(self.on_favorites_clicked)
            account_menu.addAction(favorites_action)
            
            # Watchlist
            watchlist_action = QAction("My watch list", self)
            watchlist_action.triggered.connect(self.on_watchlist_clicked)
            account_menu.addAction(watchlist_action)
            
            # Genre preferences
            genre_action = QAction("My genre preferences", self)
            genre_action.triggered.connect(self.on_genre_preferences_clicked)
            account_menu.addAction(genre_action)
            
            account_menu.addSeparator()
            
            # Logout
            logout_action = QAction("Logout", self)
            logout_action.triggered.connect(self.on_logout_clicked)
            account_menu.addAction(logout_action)
        else:
            # Login
            login_action = QAction("Login", self)
            login_action.triggered.connect(self.on_login_clicked)
            account_menu.addAction(login_action)
        
        self.accountButton.setMenu(account_menu)
    
    # ========== DISPLAY METHODS ==========
    
    def show_movies(self, movie_list=None):
        """
        Display a given list of movies according to the current view mode.
        
        Args:
            movie_list (list): List of movies to display.
                              If None, displays all movies.
        """
        if movie_list is None:
            movie_list = self.controller.get_all_movies()
        
        self._clear_layout(self.gridLayout)
        
        if self.current_view_mode == "genre":
            self._show_movie_list_by_genre(movie_list)
        elif self.current_view_mode == "grid":
            self._show_movie_list_by_grid(movie_list)
    
    def _show_movie_list_by_genre(self, movie_list):
        """
        Display movies organized by genre with horizontal scrolling.
        Netflix-style layout with one row per genre.
        """
        grouped_movies = self.controller.get_movies_grouped_by_genre(movie_list)
        layout = self.gridLayout
        self.displayed_cards = []
        max_col = self._calculate_columns()
        
        row = 0
        for genre, movies in grouped_movies.items():
            if movies:
                genre_row = GenreRow(genre, movies, self.user_manager)
                layout.addWidget(genre_row, row, 0, 1, max_col)
                
                for card_widget in genre_row.get_cards():
                    self._connect_card_signals(card_widget)
                    self.displayed_cards.append(card_widget)
                
                row += 1
        
        try:
            self.scrollAreaWidgetContents.adjustSize()
        except Exception:
            pass
    
    def _show_movie_list_by_grid(self, movie_list):
        """
        Update the display of movie cards with improved centering for short lists.
        
        Args:
            movie_list (list): List of movies to display.
        """
        layout = self.gridLayout
        self.displayed_cards = []
        max_col = self._calculate_columns()
        num_movies = len(movie_list)
        
        if num_movies < max_col:
            # Center a single row
            start_col = (max_col - num_movies) // 2
            row = 0
            col = start_col
            
            for film in movie_list:
                card_widget = createFilmCard(film, self.user_manager)
                self._connect_card_signals(card_widget)
                self.displayed_cards.append(card_widget)
                layout.addWidget(card_widget, row, col)
                col += 1
        else:
            # Normal grid layout
            row, col = 0, 0
            
            for film in movie_list:
                card_widget = createFilmCard(film, self.user_manager)
                self._connect_card_signals(card_widget)
                self.displayed_cards.append(card_widget)
                layout.addWidget(card_widget, row, col)
                col += 1
                if col >= max_col:
                    col = 0
                    row += 1
            
            # Center last incomplete row if needed
            last_row_items = num_movies % max_col
            if last_row_items > 0 and last_row_items < max_col // 2:
                layout.setColumnStretch(max_col, 1)
        
        try:
            self.scrollAreaWidgetContents.adjustSize()
        except Exception:
            pass
    
    def show_movie_detail_modal(self, movie):
        """
        Display the movie detail window.
        
        Args:
            movie: Movie instance to display
        """
        self.detail_window = MovieDetailModal(movie, self.user_manager, self)
        
        # Connect signals for synchronization
        self.detail_window.like_changed.connect(self._sync_all_cards_like_state)
        self.detail_window.watchlist_changed.connect(self._on_watchlist_changed)
        self.detail_window.watched_changed.connect(self._on_watched_changed)
        
        self.detail_window.show()
    
    # ========== UTILITY METHODS ==========
    
    def _calculate_columns(self):
        """Dynamically calculates the number of columns based on available width."""
        card_width = 300
        min_columns = 2
        max_columns = 5
        default_columns = 3
        
        available_width = self.scrollArea.width() - 40
        
        if available_width < 400:
            return default_columns
        
        columns = max(min_columns, min(max_columns, available_width // card_width))
        return columns
    
    def _clear_layout(self, layout):
        """
        Private helper to properly clear a layout.
        
        Args:
            layout: QLayout to clear
        """
        self.displayed_cards.clear()
        
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout:
                    self._clear_layout(sub_layout)
    
    def _connect_card_signals(self, card):
        """
        Connect the signals of a movie card for synchronization.
        
        Args:
            card: FilmCard instance
        """
        card.like_changed.connect(self._sync_all_cards_like_state)
        card.play_clicked.connect(self.show_movie_detail_modal)
    
    # ========== SYNCHRONIZATION METHODS ==========
    
    def _sync_all_cards_like_state(self, film_id, is_liked):
        """
        Synchronize the like state of all displayed cards for a given movie.
        
        Args:
            film_id: Movie identifier
            is_liked: New like state
        """
        # Filter out deleted cards
        valid_cards = []
        for card in self.displayed_cards:
            try:
                if card.parent() is not None and hasattr(card, 'sync_like_state'):
                    card.sync_like_state(film_id, is_liked)
                    valid_cards.append(card)
            except RuntimeError:
                pass
        
        self.displayed_cards = valid_cards
        
        # Reload views if necessary
        if self.current_view == "favorites" and not is_liked:
            QTimer.singleShot(200, self._reload_favorites_view)
        elif self.current_view == "recommendation":
            QTimer.singleShot(200, self._reload_recomandation_vue)
    
    def _on_watchlist_changed(self, movie_id, is_in_watchlist):
        """
        Handle watchlist change from movie detail modal.
        
        Args:
            movie_id: Movie identifier
            is_in_watchlist: New watchlist state
        """
        print(f"Watchlist changed for {movie_id}: {is_in_watchlist}")
        
        # Update modal button if still open
        if hasattr(self, 'detail_window') and self.detail_window.isVisible():
            self.detail_window.update_watchlist_button()
        
        # Reload watchlist view if active
        if self.current_view == "watchlist" and not is_in_watchlist:
            print("Reloading watchlist view...")
            user = self.user_manager.current_user
            if user:
                watchlist = self.controller.get_wathclist_movie(user)
                
                if not watchlist:
                    print("Watchlist is now empty")
                    self._clear_layout(self.gridLayout)
                else:
                    self.show_movies(watchlist)
    
    def _on_watched_changed(self, movie_id, is_watched):
        """
        Handle watched status change from movie detail modal.
        
        Args:
            movie_id: Movie identifier
            is_watched: New watched state
        """
        print(f"Watched status changed for {movie_id}: {is_watched}")
        
        # Auto-remove from watchlist when marked as watched
        if is_watched:
            user = self.user_manager.current_user
            if user and user.is_in_watchlist(movie_id):
                user.remove_from_watchlist(movie_id)
                self.user_manager.save_users()
                print(f"Removed {movie_id} from watchlist (marked as watched)")
                
                if hasattr(self, 'detail_window') and self.detail_window.isVisible():
                    self.detail_window.update_watchlist_button()
        
        # Update modal buttons
        if hasattr(self, 'detail_window') and self.detail_window.isVisible():
            self.detail_window.update_watched_button()
        
        # Reload watchlist view if active
        if self.current_view == "watchlist" and is_watched:
            print("Reloading watchlist view (movie marked as watched)...")
            user = self.user_manager.current_user
            if user:
                watchlist = self.controller.get_wathclist_movie(user)
                
                if not watchlist:
                    self._clear_layout(self.gridLayout)
                else:
                    self.show_movies(watchlist)
        
        # Reload recommendations if active
        if self.current_view == "recommendation":
            print("Reloading recommendations (watched status changed)...")
            user = self.user_manager.current_user
            if user:
                recommendations = self.controller.get_recommended_movies(user)
                self.show_movies(recommendations)
    
    # ========== RELOAD METHODS ==========
    
    def _reload_favorites_view(self):
        """Fully reload the favorites view (called with delay)."""
        user = self.user_manager.current_user
        if not user or self.current_view != "favorites":
            return
        
        print(f"Reloading favorites view for {user.username}")
        favorites = self.controller.get_favorite_movies(user)
        
        if not favorites:
            print("No favorites to display")
            self._clear_layout(self.gridLayout)
        else:
            self.show_movies(favorites)
    
    def _reload_recomandation_vue(self):
        """Fully reload the recommendation view (called with delay)."""
        user = self.user_manager.current_user
        if not user or self.current_view != "recommendation":
            return
        
        print(f"Reloading recommendation view for {user.username}")
        recommendations = self.controller.get_recommended_movies(user)
        
        if not recommendations:
            print("No recommendations to display")
            self._clear_layout(self.gridLayout)
        else:
            self.show_movies(recommendations)
    
    # ========== EVENT HANDLERS - Navigation ==========
    
    def on_home_clicked(self):
        """Handler for the Home button click."""
        self.searchBar.clear()
        all_movies = self.controller.get_all_movies()
        
        self.current_view = "home"
        self.current_view_mode = "genre"
        self.show_movies(all_movies)
    
    def on_recomendation_clicked(self):
        """Handler for the Recommendation button click."""
        if not self.user_manager.current_user:
            print("Please log in to see recommendations")
            return
        
        user = self.user_manager.current_user
        self.searchBar.clear()
        
        recommendations = self.controller.get_recommended_movies(user)
        
        self.current_view = "recommendation"
        self.current_view_mode = "genre"
        self.show_movies(recommendations)
    
    def on_search_clicked(self):
        """Handler for the Search button click."""
        query = self.searchBar.text().strip()
        results = self.controller.search_movies(query)
        
        self.current_view = "search"
        self.current_view_mode = "grid"
        self.show_movies(results)
    
    # ========== EVENT HANDLERS - Account Menu ==========
    
    def on_login_clicked(self):
        """Handler for login."""
        user = show_login_dialog(self.user_manager, self)
        
        if user:
            print(f"Logged in as {user.username}")
            self.setup_account_menu()
    
    def on_logout_clicked(self):
        """Handler for logout."""
        if self.user_manager.current_user:
            if confirm_logout(self.user_manager.current_user.username, self):
                print(f"Logging out {self.user_manager.current_user.username}")
                self.user_manager.current_user = None
                self.user_manager.save_users()
                self.setup_account_menu()
        else:
            print("No user logged in")
    
    def on_genre_preferences_clicked(self):
        """Handler to display the genre preferences dialog."""
        if not self.user_manager.current_user:
            print("Please log in to manage your preferences")
            return
        
        all_genres = self.catalogue.get_all_genres()
        show_genre_preferences_dialog(self.user_manager, all_genres, self)
    
    def on_favorites_clicked(self):
        """Handler to display favorites."""
        user = self.user_manager.current_user
        if not user:
            print("Please log in to see your favorites")
            return
        
        print(f"Favorites of {user.username}: {user.favorites}")
        self.searchBar.clear()
        
        favorites = self.controller.get_favorite_movies(user)
        
        self.current_view = "favorites"
        self.current_view_mode = "grid"
        self.show_movies(favorites)
    
    def on_watchlist_clicked(self):
        """Handler to display the watchlist."""
        user = self.user_manager.current_user
        if not user:
            print("Warning: Please log in to see your list")
            return
        
        print(f"Watch list of {user.username}: {user.watchlist}")
        watchlist = self.controller.get_wathclist_movie(user)
        
        self.current_view = "watchlist"
        self.current_view_mode = "genre"
        self.show_movies(watchlist) 
    
    # ========== QT EVENT OVERRIDES ==========
    
    def resizeEvent(self, event):
        """Event handler for window resize."""
        super().resizeEvent(event)
        
        if not hasattr(self, "controller") or self.gridLayout.count() == 0:
            return
        
        # Get current search query
        current_query = ""
        try:
            current_query = self.searchBar.text().strip()
        except Exception:
            current_query = ""
        
        # Get the current list of movies to display
        if current_query:
            movie_list = self.controller.search_movies(current_query)
        else:
            if getattr(self, "current_view", "") == "favorites":
                user = getattr(self.user_manager, "current_user", None)
                movie_list = self.controller.get_favorite_movies(user) if user else []
            elif getattr(self, "current_view", "") == "recommendation":
                user = getattr(self.user_manager, "current_user", None)
                movie_list = self.controller.get_recommended_movies(user) if user else []
            elif getattr(self, "current_view", "") == "watchlist":
                user = getattr(self.user_manager, "current_user", None)
                movie_list = self.controller.get_wathclist_movie(user) if user else []
            else:
                movie_list = self.controller.get_all_movies()
        
        try:
            self.show_movies(movie_list)
        except Exception:
            pass

# ========== APPLICATION ENTRY POINT ==========

if __name__ == "__main__":
    catalog = Catalog("./csv_data/catalog.csv")
    catalog.load_from_csv()
    
    app = QApplication(sys.argv)
    
    # Load the Netflux stylesheet
    style_path = "./assets/styles.qss"
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f: 
            app.setStyleSheet(f.read())
        print("Netflux stylesheet loaded")
    else:
        print(f"Error: Stylesheet not found: {style_path}")
        raise FileNotFoundError(f"The style file '{style_path}' is missing. Please make sure it exists.")
    
    window = MainApp(catalog)
    window.show()
    sys.exit(app.exec())