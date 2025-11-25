"""
Dialogues et interfaces utilisateur pour la gestion des comptes
Sépare la logique UI complexe du fichier main.py
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QMessageBox, QFormLayout, 
                            QCheckBox, QScrollArea, QWidget, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from user_manager.user import User, UserManager


class LoginDialog(QDialog):
    """
    Dialogue de connexion/création de compte
    """
    
    def __init__(self, user_manager: UserManager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.logged_user = None  # Utilisateur connecté après le dialogue
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du dialogue"""
        self.setWindowTitle("Netflux - Login")
        self.setMinimumSize(400, 300)
        self.setModal(True)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Titre
        title = QLabel("Welcome on Netflux")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Formulaire
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Champ username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(35)
        form_layout.addRow("Username", self.username_input)
        
        
        main_layout.addLayout(form_layout)
        
        # Message d'info
        info_label = QLabel("Si le compte existe, vous serez connecté.\nSinon, un nouveau compte sera créé.")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setObjectName("infoLabel")
        main_layout.addWidget(info_label)
        
        # Spacer
        main_layout.addStretch()
        
        # Boutons
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
        
        # Appliquer l'ObjectName pour utiliser le style global
        self.setObjectName("loginDialog")
        login_btn.setObjectName("primaryButton")
    
    def on_login(self):
        """Gère la connexion ou création de compte"""
        username = self.username_input.text().strip()
        
        if not username:
            QMessageBox.warning(self, "Erreur", "Please enter a username")
            return
        
        # Chercher si l'utilisateur existe
        existing_user = self.user_manager.get_user_by_username(username)
        
        if existing_user:
            # Connexion à un compte existant
            self.user_manager.set_current_user(existing_user)
            self.logged_user = existing_user
            
        else:
            # Créer un nouveau compte
            new_user = self.user_manager.create_user(username)
            self.logged_user = new_user
            QMessageBox.information(self, "Registration successful", 
                                  f"Welcome {username} !\nYour account has been created successfully.")
        
        self.accept()

def show_login_dialog(user_manager: UserManager, parent=None) :
    """
    Affiche le dialogue de connexion et retourne l'utilisateur connecté
    
    Args:
        user_manager: Gestionnaire d'utilisateurs
        parent: Widget parent
        
    Returns:
        User si connexion réussie, None sinon
    """
    dialog = LoginDialog(user_manager, parent)
    result = dialog.exec()
    
    if result == QDialog.DialogCode.Accepted:
        return dialog.logged_user
    return None


def confirm_logout(username: str, parent=None) -> bool:
    """
    Demande confirmation avant déconnexion
    
    Args:
        username: Nom de l'utilisateur
        parent: Widget parent
        
    Returns:
        True si l'utilisateur confirme, False sinon
    """
    reply = QMessageBox.question(
        parent,
        "Déconnexion",
        f"Voulez-vous vraiment vous déconnecter ({username}) ?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    return reply == QMessageBox.StandardButton.Yes




class GenrePreferencesDialog(QDialog):
    """
    Dialogue pour gérer les préférences de genres de l'utilisateur
    """
    def __init__(self, user_manager: UserManager, genre_list=None, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.genre_list = genre_list if genre_list else []
        self.checkboxes = {}  # Dictionnaire pour stocker les checkboxes {genre: checkbox}
        
        if user_manager.current_user:
            self.user = user_manager.current_user
        else:
            self.user = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du dialogue"""
        self.setWindowTitle("Netflux - Genre Preferences")
        self.setMinimumSize(500, 600)
        self.setModal(True)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Titre
        title = QLabel("Select Your Favorite Genres")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Sous-titre avec nom d'utilisateur
        if self.user:
            subtitle = QLabel(f"Preferences for {self.user.username}")
            subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subtitle.setObjectName("infoLabel")
            main_layout.addWidget(subtitle)
        
        # Zone scrollable pour les genres
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(350)
        
        # Widget conteneur pour les checkboxes
        genres_container = QWidget()
        genres_layout = QGridLayout(genres_container)
        genres_layout.setSpacing(15)
        
        # Créer une checkbox pour chaque genre (2 colonnes)
        row, col = 0, 0
        for genre in self.genre_list:
            checkbox = QCheckBox(genre)
            checkbox.setMinimumHeight(30)
            
            # Cocher si le genre est déjà dans les préférences de l'utilisateur
            if self.user and genre in self.user.likedGenre:
                checkbox.setChecked(True)
            
            self.checkboxes[genre] = checkbox
            genres_layout.addWidget(checkbox, row, col)
            
            col += 1
            if col >= 2:  # 2 colonnes
                col = 0
                row += 1
        
        scroll_area.setWidget(genres_container)
        main_layout.addWidget(scroll_area)
        
        # Spacer
        main_layout.addStretch()
        
        # Boutons
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
        
        # Appliquer l'ObjectName pour le style
        self.setObjectName("loginDialog")
    
    def save_preferences(self):
        """Sauvegarde les préférences de genres"""
        if not self.user:
            QMessageBox.warning(self, "Error", "No user logged in")
            return
        
        # Récupérer les genres cochés
        selected_genres = []
        for genre, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                selected_genres.append(genre)
        
        # Sauvegarder dans l'utilisateur
        self.user.likedGenre = selected_genres
        
        # Sauvegarder dans le fichier
        self.user_manager.save_users()
        
        QMessageBox.information(self, "Success", 
                              f"{len(selected_genres)} genre(s) saved successfully!")
        self.accept()


def show_genre_preferences_dialog(user_manager: UserManager, genre_list, parent=None):
    """
    Affiche le dialogue de préférences de genres
    
    Args:
        user_manager: Gestionnaire d'utilisateurs
        genre_list: Liste des genres disponibles
        parent: Widget parent
        
    Returns:
        True si sauvegarde réussie, False sinon
    """
    dialog = GenrePreferencesDialog(user_manager, genre_list, parent)
    result = dialog.exec()
    return result == QDialog.DialogCode.Accepted
