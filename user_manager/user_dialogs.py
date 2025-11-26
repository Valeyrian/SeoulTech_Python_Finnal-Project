"""
Dialogs and user interfaces for account management.
Separates complex UI logic from the main.py file.
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QMessageBox, QFormLayout, 
                            QCheckBox, QScrollArea, QWidget, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from user_manager.user import UserManager


class LoginDialog(QDialog):
    """
    Login/account creation dialog.
    """
    
    def __init__(self, user_manager: UserManager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.logged_user = None  # User logged in after the dialog
        self.setup_ui()
    
    def setup_ui(self):
        """Configure the dialog interface."""
        self.setWindowTitle("Netflux - Login")
        self.setMinimumSize(400, 300)
        self.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Welcome on Netflux")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(35)
        form_layout.addRow("Username", self.username_input)
        
        
        main_layout.addLayout(form_layout)
        
        # Info message
        info_label = QLabel("If the account exists, you will be logged in.\nOtherwise, a new account will be created.")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setObjectName("infoLabel")
        main_layout.addWidget(info_label)
        
        # Spacer
        main_layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        login_btn = QPushButton("Login")
        login_btn.setMinimumHeight(40)
        login_btn.setObjectName("loginButton")
        login_btn.clicked.connect(self.on_login)
        login_btn.setDefault(True)
        button_layout.addWidget(login_btn)
        
        main_layout.addLayout(button_layout)
        
        # Apply ObjectName to use global style
        self.setObjectName("loginDialog")
        login_btn.setObjectName("primaryButton")
    
    def on_login(self):
        """Handle login or account creation."""
        username = self.username_input.text().strip()
        
        if not username:
            QMessageBox.warning(self, "Error", "Please enter a username")
            return
        
        # Check if user exists
        existing_user = self.user_manager.get_user_by_username(username)
        
        if existing_user:
            # Log in to existing account
            self.user_manager.set_current_user(existing_user)
            self.logged_user = existing_user
            
        else:
            # Create a new account
            new_user = self.user_manager.create_user(username)
            self.logged_user = new_user
            QMessageBox.information(self, "Registration successful", 
                                  f"Welcome {username} !\nYour account has been created successfully.")
        
        self.accept()

def show_login_dialog(user_manager: UserManager, parent=None) :
    """
    Display the login dialog and return the logged-in user.
    
    Args:
        user_manager: User manager
        parent: Parent widget
        
    Returns:
        User if login successful, None otherwise
    """
    dialog = LoginDialog(user_manager, parent)
    result = dialog.exec()
    
    if result == QDialog.DialogCode.Accepted:
        return dialog.logged_user
    return None


def confirm_logout(username: str, parent=None) -> bool:
    """
    Ask for confirmation before logout.
    
    Args:
        username: User's name
        parent: Parent widget
        
    Returns:
        True if user confirms, False otherwise
    """
    reply = QMessageBox.question(
        parent,
        "Logout",
        f"Do you really want to log out ({username})?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    return reply == QMessageBox.StandardButton.Yes




class GenrePreferencesDialog(QDialog):
    """
    Dialog for managing the user's genre preferences.
    """
    def __init__(self, user_manager: UserManager, genre_list=None, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.genre_list = genre_list if genre_list else []
        self.checkboxes = {}  # Dictionary to store checkboxes {genre: checkbox}
        
        if user_manager.current_user:
            self.user = user_manager.current_user
        else:
            self.user = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configure the dialog interface."""
        self.setWindowTitle("Netflux - Genre Preferences")
        self.setMinimumSize(500, 600)
        self.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Select Your Favorite Genres")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Subtitle with username
        if self.user:
            subtitle = QLabel(f"Preferences for {self.user.username}")
            subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subtitle.setObjectName("infoLabel")
            main_layout.addWidget(subtitle)
        
        # Scrollable area for genres
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(350)
        
        # Container widget for checkboxes
        genres_container = QWidget()
        genres_layout = QGridLayout(genres_container)
        genres_layout.setSpacing(15)
        
        # Create a checkbox for each genre (2 columns)
        row, col = 0, 0
        for genre in self.genre_list:
            checkbox = QCheckBox(genre)
            checkbox.setMinimumHeight(30)
            
            # Check if the genre is already in user preferences
            if self.user and hasattr(self.user, 'liked_genres') and genre in self.user.liked_genres:
                checkbox.setChecked(True)
            elif self.user and hasattr(self.user, 'likedGenre') and genre in self.user.likedGenre:
                checkbox.setChecked(True)
            
            self.checkboxes[genre] = checkbox
            genres_layout.addWidget(checkbox, row, col)
            
            col += 1
            if col >= 2:
                col = 0
                row += 1
        
        scroll_area.setWidget(genres_container)
        main_layout.addWidget(scroll_area)
        
        # Spacer
        main_layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Preferences")
        save_btn.setMinimumHeight(40)
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_preferences)
        save_btn.setDefault(True)
        button_layout.addWidget(save_btn)
        
        main_layout.addLayout(button_layout)
        
        # Apply ObjectName for styling
        self.setObjectName("loginDialog")
    
    def save_preferences(self):
        """Save genre preferences."""
        if not self.user:
            QMessageBox.warning(self, "Error", "No user logged in")
            return
        
        # Get selected genres
        selected_genres = []
        for genre, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                selected_genres.append(genre)
        
        # Save in user (support both attribute names)
        if hasattr(self.user, 'liked_genres'):
            self.user.liked_genres = selected_genres
        if hasattr(self.user, 'likedGenre'):
            self.user.likedGenre = selected_genres
        
        # Save to file
        self.user_manager.save_users()
        
        QMessageBox.information(self, "Success", 
                              f"{len(selected_genres)} genre(s) saved successfully!")
        self.accept()


def show_genre_preferences_dialog(user_manager: UserManager, genre_list, parent=None):
    """
    Display the genre preferences dialog.
    
    Args:
        user_manager: User manager
        genre_list: List of available genres
        parent: Parent widget
        
    Returns:
        True if save successful, False otherwise
    """
    dialog = GenrePreferencesDialog(user_manager, genre_list, parent)
    result = dialog.exec()
    return result == QDialog.DialogCode.Accepted
