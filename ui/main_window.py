from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    """
    UI class for the main window of the application.
    This class sets up the user interface for the main window, which includes:
    - A header section with navigation buttons and search functionality
    - A logo display area
    - Navigation buttons for Home and Recommendations pages
    - A search bar with a search button for content discovery
    - An account management button with dropdown menu
    - A scrollable content area using QScrollArea for displaying dynamic content
    - Standard menu bar and status bar
    The layout uses:
    - QVBoxLayout for the main vertical structure
    - QHBoxLayout for the horizontal header arrangement
    - QGridLayout for the scrollable content area
    Attributes:
        centralwidget (QWidget): The main central widget of the window
        header (QWidget): Container for the header section with navigation and search
        logo (QLabel): Label for displaying the application logo
        acceuilButton (QPushButton): Button to navigate to the home page
        recomandationButton (QPushButton): Button to navigate to the recommendations page
        searchBar (QLineEdit): Input field for search queries
        searchButton (QPushButton): Button to trigger search action
        accountButton (QToolButton): Dropdown button for account-related actions
        scrollArea (QScrollArea): Scrollable area for main content display
        scrollAreaWidgetContents (QWidget): Container widget within the scroll area
        gridLayout (QGridLayout): Grid layout for organizing content in the scroll area
        menubar (QMenuBar): Standard menu bar at the top of the window
        statusbar (QStatusBar): Status bar at the bottom of the window
    Methods:
        setupUi(MainWindow): Initializes and configures all UI components
        retranslateUi(MainWindow): Sets up translatable text for internationalization support
    """
    
    def _create_expanding_size_policy(self, widget):
        """Create and apply an expanding size policy."""
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, 
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
    
    def _create_horizontal_expanding_size_policy(self, widget):
        """Create and apply a horizontal expanding size policy."""
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, 
            QtWidgets.QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
    
    def _create_fixed_size_policy(self, widget):
        """Create and apply a fixed size policy."""
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, 
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
    
    def _setup_central_widget(self, MainWindow):
        """Setup the central widget and its layout."""
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self._create_expanding_size_policy(self.centralwidget)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
    
    def _setup_header(self):
        """Setup the header widget with all navigation elements."""
        self.header = QtWidgets.QWidget(parent=self.centralwidget)
        self._create_horizontal_expanding_size_policy(self.header)
        self.header.setMinimumSize(QtCore.QSize(0, 32))
        self.header.setStyleSheet("")
        self.header.setObjectName("header")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.header)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self._setup_logo()
        self._setup_navigation_buttons()
        self._setup_search_bar()
        self._setup_account_button()
        
        self.verticalLayout.addWidget(self.header)
    
    def _setup_logo(self):
        """Setup the logo label."""
        self.logo = QtWidgets.QLabel(parent=self.header)
        self._create_fixed_size_policy(self.logo)
        self.logo.setMinimumSize(QtCore.QSize(80, 32))
        self.logo.setText("")
        self.logo.setObjectName("logo")
        self.horizontalLayout.addWidget(self.logo)
    
    def _setup_navigation_buttons(self):
        """Setup navigation buttons (Home and Recommendations)."""
        self.acceuilButton = QtWidgets.QPushButton(parent=self.header)
        self.acceuilButton.setMinimumSize(QtCore.QSize(0, 32))
        self.acceuilButton.setObjectName("acceuilButton")
        self.horizontalLayout.addWidget(self.acceuilButton)
        
        self.recomandationButton = QtWidgets.QPushButton(parent=self.header)
        self.recomandationButton.setMinimumSize(QtCore.QSize(0, 32))
        self.recomandationButton.setObjectName("recomandationButton")
        self.horizontalLayout.addWidget(self.recomandationButton)
    
    def _setup_search_bar(self):
        """Setup search bar and search button."""
        spacerItem = QtWidgets.QSpacerItem(
            15, 20, 
            QtWidgets.QSizePolicy.Policy.Fixed, 
            QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        
        self.searchBar = QtWidgets.QLineEdit(parent=self.header)
        self.searchBar.setMinimumSize(QtCore.QSize(70, 32))
        self.searchBar.setText("")
        self.searchBar.setObjectName("searchBar")
        self.horizontalLayout.addWidget(self.searchBar)
        
        self.searchButton = QtWidgets.QPushButton(parent=self.header)
        self.searchButton.setMinimumSize(QtCore.QSize(0, 32))
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout.addWidget(self.searchButton)
    
    def _setup_account_button(self):
        """Setup account dropdown button."""
        self.accountButton = QtWidgets.QToolButton(parent=self.header)
        self.accountButton.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        self.accountButton.setFont(font)
        self.accountButton.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        self.accountButton.setObjectName("accountButton")
        self.horizontalLayout.addWidget(self.accountButton)
    
    def _setup_scroll_area(self):
        """Setup the scrollable content area."""
        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 807, 451))
        self._create_expanding_size_policy(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
    
    def _setup_menu_and_status_bar(self, MainWindow):
        """Setup menubar and statusbar."""
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 833, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
    
    def setupUi(self, MainWindow):
        """Initialize and configure all UI components."""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(833, 594)
        MainWindow.setStyleSheet("")
        
        self._setup_central_widget(MainWindow)
        self._setup_header()
        self._setup_scroll_area()
        MainWindow.setCentralWidget(self.centralwidget)
        self._setup_menu_and_status_bar(MainWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.acceuilButton.setText(_translate("MainWindow", "Home"))
        self.recomandationButton.setText(_translate("MainWindow", "Recommendations"))
        self.searchBar.setPlaceholderText(_translate("MainWindow", "Search for your content!"))
        self.searchButton.setText(_translate("MainWindow", "go"))
        self.accountButton.setText(_translate("MainWindow", "Account"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
