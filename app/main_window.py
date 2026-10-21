from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


APP_STYLESHEET = """
QMainWindow, QWidget {
    background-color: #111827;
    color: #E5E7EB;
    font-family: "Segoe UI";
    font-size: 13px;
}

QFrame#sidebar {
    background-color: #0B1220;
    border-right: 1px solid #263247;
}

QLabel#app_title {
    font-size: 23px;
    font-weight: bold;
    color: #F9FAFB;
}

QLabel#app_subtitle {
    color: #94A3B8;
    font-size: 12px;
}

QLabel#profile_name {
    font-weight: bold;
    color: #F9FAFB;
}

QLabel#profile_subtitle {
    color: #94A3B8;
    font-size: 11px;
}

QLabel#page_title {
    font-size: 27px;
    font-weight: bold;
    color: #F9FAFB;
}

QLabel#page_description {
    color: #94A3B8;
    font-size: 13px;
}

QPushButton {
    background-color: transparent;
    color: #CBD5E1;
    border: none;
    border-radius: 7px;
    padding: 11px 12px;
    text-align: left;
}

QPushButton:hover {
    background-color: #1E293B;
    color: #FFFFFF;
}

QPushButton:checked {
    background-color: #1D4ED8;
    color: #FFFFFF;
    font-weight: bold;
}

QPushButton#quick_button {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 16px;
    color: #F9FAFB;
}

QPushButton#quick_button:hover {
    background-color: #263750;
    border: 1px solid #3B82F6;
}

QFrame#panel {
    background-color: #172033;
    border: 1px solid #29364D;
    border-radius: 12px;
}

QLabel#panel_title {
    font-size: 18px;
    font-weight: bold;
    color: #F9FAFB;
}

QLabel#panel_text {
    color: #CBD5E1;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Utility Hub")
        self.resize(1150, 760)
        self.setMinimumSize(850, 600)
        self.setStyleSheet(APP_STYLESHEET)

        self.navigation_buttons = {}
        self.pages = {}

        self.build_interface()

    def build_interface(self):
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = self.build_sidebar()
        content = self.build_content_area()

        root_layout.addWidget(sidebar)
        root_layout.addWidget(content, 1)

        self.setCentralWidget(root)
        self.show_page("Home")

    def build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(225)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 24, 16, 18)
        layout.setSpacing(8)

        title = QLabel("UTILITY HUB")
        title.setObjectName("app_title")

        subtitle = QLabel("PERSONAL DESKTOP")
        subtitle.setObjectName("app_subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(22)

        profile_button = QPushButton("  U    Your Name")
        profile_button.setCheckable(False)
        profile_button.setToolTip("Your personal workspace")
        layout.addWidget(profile_button)

        profile_subtitle = QLabel("       My Workspace")
        profile_subtitle.setObjectName("profile_subtitle")
        layout.addWidget(profile_subtitle)
        layout.addSpacing(20)

        navigation_items = [
            ("Home", "⌂"),
            ("System", "▤"),
            ("Applications", "▦"),
            ("Scripts", "⌘"),
            ("Cybersecurity", "◈"),
            ("My Projects", "▣"),
            ("Notes", "☰"),
        ]

        for page_name, symbol in navigation_items:
            button = QPushButton(f"{symbol}   {page_name}")
            button.setCheckable(True)
            button.clicked.connect(
                lambda checked=False, name=page_name: self.show_page(name)
            )
            self.navigation_buttons[page_name] = button
            layout.addWidget(button)

        layout.addStretch()

        settings_button = QPushButton("⚙   Settings")
        settings_button.setCheckable(True)
        settings_button.clicked.connect(
            lambda checked=False: self.show_page("Settings")
        )
        self.navigation_buttons["Settings"] = settings_button
        layout.addWidget(settings_button)

        return sidebar

    def build_content_area(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 28, 30, 28)

        self.page_stack = QStackedWidget()
        layout.addWidget(self.page_stack)

        page_names = [
            "Home",
            "System",
            "Applications",
            "Scripts",
            "Cybersecurity",
            "My Projects",
            "Notes",
            "Settings",
        ]

        for page_name in page_names:
            page = self.build_page(page_name)
            self.pages[page_name] = page
            self.page_stack.addWidget(page)

        return content

    def build_page(self, page_name):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel(page_name)
        title.setObjectName("page_title")
        layout.addWidget(title)

        descriptions = {
            "Home": "Your personal desktop environment and quick-access workspace.",
            "System": "View system information and resource usage.",
            "Applications": "Organize and launch your applications.",
            "Scripts": "Access your Python scripts and automation tools.",
            "Cybersecurity": "Your cybersecurity tools and lab shortcuts.",
            "My Projects": "Keep your development projects organized.",
            "Notes": "Your personal notes and quick references.",
            "Settings": "Customize your Utility Hub experience.",
        }

        description = QLabel(descriptions.get(page_name, ""))
        description.setObjectName("page_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        if page_name == "Home":
            self.build_home_page(layout)
        elif page_name != "Settings":
            self.build_placeholder_page(layout, page_name)

        layout.addStretch()
        return page

    def build_home_page(self, layout):
        section_title = QLabel("Quick Access")
        section_title.setObjectName("panel_title")
        layout.addWidget(section_title)

        quick_access_items = [
            ("System Overview", "System"),
            ("Applications", "Applications"),
            ("Scripts & Automation", "Scripts"),
            ("Cybersecurity Lab", "Cybersecurity"),
            ("My Projects", "My Projects"),
            ("Notes", "Notes"),
        ]

        for label, target_page in quick_access_items:
            button = QPushButton(label)
            button.setObjectName("quick_button")
            button.setMinimumHeight(55)
            button.clicked.connect(
                lambda checked=False, name=target_page: self.show_page(name)
            )
            layout.addWidget(button)

        panel = QFrame()
        panel.setObjectName("panel")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 18, 20, 18)
        panel_layout.setSpacing(8)

        welcome_title = QLabel("Welcome to Utility Hub")
        welcome_title.setObjectName("panel_title")

        welcome_text = QLabel(
            "A central place for your applications, system tools, "
            "cybersecurity utilities, scripts, and personal projects."
        )
        welcome_text.setObjectName("panel_text")
        welcome_text.setWordWrap(True)

        panel_layout.addWidget(welcome_title)
        panel_layout.addWidget(welcome_text)
        layout.addWidget(panel)

    def build_placeholder_page(self, layout, page_name):
        panel = QFrame()
        panel.setObjectName("panel")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 20, 20, 20)

        message = QLabel(
            f"The {page_name} page is ready for future features."
        )
        message.setObjectName("panel_text")
        message.setWordWrap(True)

        panel_layout.addWidget(message)
        layout.addWidget(panel)

    def show_page(self, page_name):
        if page_name not in self.pages:
            return

        self.page_stack.setCurrentWidget(self.pages[page_name])

        for name, button in self.navigation_buttons.items():
            button.setChecked(name == page_name)
