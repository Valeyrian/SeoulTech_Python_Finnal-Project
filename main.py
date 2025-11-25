import sys
from unittest import case
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenu
from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from ui.main_window import Ui_MainWindow
from controllers.movie_controller import MovieController
from genre_row import GenreRow
from models import Catalogue, Film
from card import createFilmCard
import os
from user_manager.user import UserManager
from user_manager.user_dialogs import show_login_dialog, confirm_logout, show_genre_preferences_dialog
from player.player import player

class MainApp(QMainWindow, Ui_MainWindow):
    """
    Main view of the Netflux application.
    
    Responsibilities:
        - UI display and user interactions
        - Does NOT contain business logic (delegated to the controller)
    """
    
    def __init__(self, catalogue):
        super().__init__()
        self.setupUi(self)  
        self.setWindowTitle("Netflux")

        if (not os.path.exists("./assets/logo.png")):
            pixmap = QPixmap("./assets/file_not_found.jpeg")
            raise FileNotFoundError("The file './assets/logo.png' is missing. Please make sure it exists.")
        else :
            pixmap = QPixmap("./assets/logo.png")

        self.logo.setPixmap(pixmap.scaled(140, 40))

        
        # Initialize the user manager
        self.user_manager = UserManager()
        self.user_manager.load_users()
        
        # Store the catalogue to access genres
        self.catalogue = catalogue
        
        # Initialize the controller (business logic layer)
        self.controller = MovieController(catalogue)
        
        self.current_view = "home"
        self.current_view_mode = "genre"
       
        self.show_movie_list_by_genre()  # Genre view with horizontal scroll
       
        
        # List to store all displayed cards (for synchronization)
        self.displayed_cards = []
        
        # Connect UI events
        self.searchButton.clicked.connect(self.on_search_clicked)
        self.searchBar.returnPressed.connect(self.on_search_clicked)
        
        # Home button: display all movies by genre
        self.acceuilButton.clicked.connect(self.on_home_clicked)

        # Recommendation button
        self.recomandationButton.clicked.connect(self.on_recomendation_clicked)
        
        # Dropdown menu for the Account button
        self.setup_account_menu()
        
    
    # ========== UI METHODS (Display only) ==========
    
    def setup_account_menu(self):
        """
        Configure the dropdown menu for the Account button.
        Displays Login or Logout depending on the connection status.
        """
        # Create the menu
        account_menu = QMenu(self)
        account_menu.setObjectName("accountMenu")
        
        # Check if a user is logged in
        if self.user_manager.current_user:
            # User logged in: display profile and logout options
            user = self.user_manager.current_user
            
            # Display the username (clickable to view profile)
            profile_action = QAction(f"{user.username}", self)
            profile_action.setEnabled(False)
            account_menu.addAction(profile_action)
            
            account_menu.addSeparator()
            
            # Favorites option
            favorites_action = QAction("My likes", self)
            favorites_action.triggered.connect(self.on_favorites_clicked)
            account_menu.addAction(favorites_action)
            
            # # Watchlist option
            # watchlist_action = QAction("My watch list", self)
            # watchlist_action.triggered.connect(self.on_watchlist_clicked)
            # account_menu.addAction(watchlist_action)

            genre_action = QAction("My genre preferences", self)
            genre_action.triggered.connect(self.on_genre_preferences_clicked)
            account_menu.addAction(genre_action)
            
            account_menu.addSeparator()
            
            # Logout button
            logout_action = QAction("Logout", self)
            logout_action.triggered.connect(self.on_logout_clicked)
            account_menu.addAction(logout_action)
        else:
            # No user logged in: display login
            login_action = QAction("Login", self)
            login_action.triggered.connect(self.on_login_clicked)
            account_menu.addAction(login_action)
        
        # Attach the menu to the button
        self.accountButton.setMenu(account_menu)
    
    def _calculate_columns(self):
        """
        Dynamically calculates the number of columns based on available width.
        """
        card_width = 300  # Approximate width of a card (280px + margins)
        min_columns = 2   # Minimum number of columns
        max_columns = 5   # Maximum number of columns (wider cards)
        default_columns = 3  # Default value at startup
        
        # Get the available width in the content area
        available_width = self.scrollArea.width() - 40  # Account for margins
        
        # If the window is not yet displayed (width too small), use default value
        if available_width < 400:  # Reasonable minimum width
            return default_columns
        
        # Calculate the optimal number of columns
        columns = max(min_columns, min(max_columns, available_width // card_width))
        
        return columns
    
    def _connect_card_signals(self, card):
        """
        Connect the signals of a movie card for synchronization.
        
        Args:
            card: FilmCard instance
        """
        # Connect the like status change signal
        card.like_changed.connect(self._sync_all_cards_like_state)
        #card.play_clicked.connect(self.startMediaPlayer)
    
    def _sync_all_cards_like_state(self, film_id, is_liked):
        """
        Synchronize the like state of all displayed cards for a given movie.
        
        Args:
            film_id: Movie identifier
            is_liked: New like state
        """

        # Iterate through all displayed cards
        for card in self.displayed_cards:
            if hasattr(card, 'sync_like_state'):
                card.sync_like_state(film_id, is_liked)

        if self.current_view_mode == "favorites":
            # If in favorites view, refresh display to remove unliked movies
            QTimer.singleShot(100, self._reload_favorites_view)
    
    def resizeEvent(self, event):
        """
        Event handler for window resize.
        Reorganizes cards when the window size changes.
        """
        super().resizeEvent(event)
        
        # Redisplay movies with the new column count
        if hasattr(self, 'controller') and self.gridLayout.count() > 0:
            # Check if we're in grid mode or genre mode
            first_item = self.gridLayout.itemAt(0)
            if first_item and first_item.widget():
                if isinstance(first_item.widget(), GenreRow):
                    # Genre mode: reorganize GenreRows with new span
                    current_query = self.searchBar.text().strip()
                    if current_query:
                        movie_list = self.controller.search_movies(current_query)
                    else:
                        movie_list = self.controller.get_all_movies()
                    self.show_movie_list_by_genre(movie_list)
                else:
                    # Grid mode: reorganize cards
                    current_query = self.searchBar.text().strip()
                    if current_query:
                        movie_list = self.controller.search_movies(current_query)
                    else:
                        movie_list = self.controller.get_all_movies()
                    self.show_movie_list(movie_list)
    
    def show_movie_list(self, movie_list=None):
        """
        Update the display of movie cards.
        
        Args:
            movie_list (list, optional): List of movies to display.
                                        If None, requests movies from the controller.
        """
        # If no list provided, request from controller
        if movie_list is None:
            movie_list = self.controller.get_all_movies()
        
        # Use the layout dedicated to movies (defined in main_window.py)
        layout = self.gridLayout
        
        # Properly clear old cards
        self._clear_layout(layout)
        
        # Reset the list of displayed cards
        self.displayed_cards = []
        
        # Add new cards in grid layout
        row, col = 0, 0
        max_col = self._calculate_columns()  # Dynamic column count calculation
        
        for film in movie_list:
            card_widget = createFilmCard(film, self.user_manager)
            
            # Connect card signals
            self._connect_card_signals(card_widget)
            
            # Register the card for synchronization
            self.displayed_cards.append(card_widget)
            
            layout.addWidget(card_widget, row, col)
            col += 1
            if col >= max_col:
                col = 0
                row += 1
        
        # Force scroll area update
        try:
            self.scrollAreaWidgetContents.adjustSize()
        except Exception:
            pass
    
    def show_movie_list_by_genre(self,movie_list=None):
        """
        Display movies organized by genre with horizontal scrolling.
        Netflix-style layout with one row per genre.
        """
        # Get movies grouped by genre from the controller
        if movie_list is None:
            movie_list = self.controller.get_all_movies()
        grouped_movies = self.controller.get_movies_grouped_by_genre(movie_list)
        
        # Clear the current layout
        layout = self.gridLayout
        self._clear_layout(layout)
        
        # Reset the list of displayed cards
        self.displayed_cards = []
        
        # Calculate the number of columns for span
        max_col = self._calculate_columns()
        
        # Create a vertical container for all genre rows
        row = 0
        for genre, films in grouped_movies.items():
            if films:  # Only if the genre has movies
                # Create a genre row with horizontal scroll
                genre_row = GenreRow(genre, films, self.user_manager)
                layout.addWidget(genre_row, row, 0, 1, max_col)  # Takes full width (dynamic)
                
                # Register all cards from this row and connect their signals
                for card_widget in genre_row.get_cards():
                    self._connect_card_signals(card_widget)
                    self.displayed_cards.append(card_widget)
                
                row += 1
        
        # Force update
        try:
            self.scrollAreaWidgetContents.adjustSize()
        except Exception:
            pass

    def show_movies(self,movie_list):
        """
        Display a given list of movies according to the current view mode.
        
        Args:
            movie_list (list): List of movies to display
        """
        self._clear_layout(self.gridLayout)

        if self.current_view_mode == "genre":
            self.show_movie_list_by_genre(movie_list)
        elif self.current_view_mode == "grid":
            self.show_movie_list(movie_list)
            
    def _clear_layout(self, layout):
        """
        Private helper to properly clear a layout.
        
        Args:
            layout: QLayout to clear
        """
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            else:
                # Handle sub-layouts if necessary
                sub_layout = item.layout()
                if sub_layout:
                    self._clear_layout(sub_layout)
    
  ##  def playVideo(self, movie):
       ## player.startMediaPlayer(movie)
        
        
   
    # ========== EVENT HANDLERS ==========
    
    def on_home_clicked(self):
        """
        Handler for the Home button click.
        Resets the search and displays all movies.
        """
        # Clear the search bar
        self.searchBar.clear()
        
        # Request all movies from the controller
        all_movies = self.controller.get_all_movies()
        
        # Update the display
        self.current_view = "home"
        self.current_view_mode = "genre"
        self.show_movies(all_movies)
        
    def on_recomendation_clicked(self):
        """ 
        Handler for the Recommendation button click.
        Delegates recommendation logic to the controller.
        """
        if not self.user_manager.current_user:
            print("Please log in to see recommendations")
            return
        
        user = self.user_manager.current_user
        
        # Request recommendations for the user from the controller
        recommendations = self.controller.get_recommanded_movies(user)
        
        # Update the display (UI logic)
        self.current_view = "recommendation"
        self.current_view_mode = "genre"
        self.show_movies(recommendations)
    
    def on_search_clicked(self):
        """
        Handler for the Search button click (or Enter key in the search bar).
        Delegates the search to the controller.
        """
        query = self.searchBar.text().strip()
        
        # Ask the controller to perform the search (business logic)
        results = self.controller.search_movies(query)
        
        # Update the display (UI logic)
        self.current_view = "search"
        self.current_view_mode = "grid"
        self.show_movies(results)



    # ========== ACCOUNT MENU HANDLERS ==========
    
    def on_login_clicked(self):
        """
        Handler for login.
        Displays the login dialog.
        """
        user = show_login_dialog(self.user_manager, self)
        
        if user:
            print(f"Logged in as {user.username}")
            # Refresh the menu to display logout
            self.setup_account_menu()
    
    def on_genre_preferences_clicked(self):
        """
        Handler to display the genre preferences dialog.
        """
        if not self.user_manager.current_user:
            print("Please log in to manage your preferences")
            return
        
        # Get the list of all genres from the catalogue
        all_genres = self.catalogue.getAllTheGenres()
        
        # Display the dialog
        show_genre_preferences_dialog(self.user_manager, all_genres, self)
    
    def on_logout_clicked(self):
        """
        Handler for logout.
        """
        if self.user_manager.current_user:
            # Ask for confirmation
            if confirm_logout(self.user_manager.current_user.username, self):
                print(f"Logging out {self.user_manager.current_user.username}")
                self.user_manager.current_user = None
                self.user_manager.save_users()
                
                # Refresh the menu to display login
                self.setup_account_menu()
        else:
            print("No user logged in")
    
    def on_favorites_clicked(self):
        """
        Handler to display favorites.
        """
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

    def _reload_favorites_view(self):
        """
        Fully reload the favorites view (called with delay).
        """
        user = self.user_manager.current_user
        if not user:
            return

        print(f"Reloading favorites view for {user.username}")
    
        favorites = self.controller.get_favorite_movies(user)

        if not favorites:
            print("No favorites to display")
            self._clear_layout(self.gridLayout)
        else:
            self.show_movies(favorites)

    def on_watchlist_clicked(self):
        """
        Handler to display the watchlist.
        """
        if not self.user_manager.current_user:
            print("Warning: Please log in to see your list")
            return
        
        user = self.user_manager.current_user
        print(f"Watch list of {user.username}: {user.watchlist}")

        
            
if __name__ == "__main__":

    catalog = Catalogue()
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
