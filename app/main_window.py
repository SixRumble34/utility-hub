from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.style import APP_STYLESHEET
from app.system_info import get_system_info


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Utility Hub")
        self.resize(1150, 760)
        self.setMinimumSize(850, 600)

        self.setStyleSheet(APP_STYLESHEET)

        self.navigation_buttons = {}
        self.pages = {}
        self.system_labels = {}
        self.system_progress_bars = {}

        self.build_interface()

        # Load the initial system readings.
        self.refresh_system_info()

        # Automatically refresh system information every second.
        self.system_refresh_timer = QTimer(self)
        self.system_refresh_timer.setInterval(1000)
        self.system_refresh_timer.timeout.connect(
            self.refresh_system_info
        )
        self.system_refresh_timer.start()

    def build_interface(self):
        """Create the main application layout."""

        central_widget = QWidget()

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = self.build_sidebar()
        content_area = self.build_content_area()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area, 1)

        self.setCentralWidget(central_widget)

        self.show_page("Home")

    def build_sidebar(self):
        """Create the sidebar and navigation buttons."""

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(14, 20, 14, 16)
        layout.setSpacing(8)

        app_title = QLabel("Utility Hub")
        app_title.setObjectName("app_title")

        layout.addWidget(app_title)
        layout.addSpacing(15)

        navigation_items = [
            ("Home", "⌂"),
            ("System", "▤"),
            ("Applications", "▦"),
            ("Scripts", "⌘"),
            ("Cybersecurity", "◈"),
            ("My Projects", "▣"),
            ("Notes", "☰"),
        ]

        for name, symbol in navigation_items:
            button = QPushButton(f"{symbol}   {name}")
            button.setObjectName("nav_button")
            button.setCheckable(True)
            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            button.clicked.connect(
                lambda checked=False, page=name: self.show_page(page)
            )

            layout.addWidget(button)
            self.navigation_buttons[name] = button

        layout.addStretch()

        settings_button = QPushButton("⚙   Settings")
        settings_button.setObjectName("settings_button")
        settings_button.setCheckable(True)
        settings_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        settings_button.clicked.connect(
            lambda checked=False: self.show_page("Settings")
        )

        layout.addWidget(settings_button)
        self.navigation_buttons["Settings"] = settings_button

        return sidebar

    def build_content_area(self):
        """Create the stacked pages in the main content area."""

        content = QWidget()
        content.setObjectName("MainContent")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 26, 30, 26)

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
        """Build a page header and its corresponding content."""

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel(page_name)
        title.setObjectName("page_title")
        layout.addWidget(title)

        descriptions = {
            "Home": (
                "Your personal desktop environment and "
                "quick-access workspace."
            ),
            "System": (
                "View system information and resource usage."
            ),
            "Applications": (
                "Organize and launch your applications."
            ),
            "Scripts": (
                "Access your Python scripts and automation tools."
            ),
            "Cybersecurity": (
                "Your cybersecurity tools and lab shortcuts."
            ),
            "My Projects": (
                "Keep your development projects organized."
            ),
            "Notes": (
                "Your personal notes and quick references."
            ),
            "Settings": (
                "Customize your Utility Hub experience."
            ),
        }

        description = QLabel(descriptions[page_name])
        description.setObjectName("page_description")
        description.setWordWrap(True)

        layout.addWidget(description)
        layout.addSpacing(12)

        if page_name == "Home":
            self.build_home_page(layout)

        elif page_name == "System":
            self.build_system_page(layout)

        else:
            self.build_placeholder_page(layout, page_name)

        layout.addStretch()

        return page

    def build_home_page(self, layout):
        """Build the Home page quick-access section."""

        quick_access_title = QLabel("Quick Access")
        quick_access_title.setObjectName("panel_title")

        layout.addWidget(quick_access_title)

        quick_access_items = [
            ("System Overview", "System"),
            ("Applications", "Applications"),
            ("Scripts & Automation", "Scripts"),
            ("Cybersecurity Lab", "Cybersecurity"),
            ("My Projects", "My Projects"),
            ("Notes", "Notes"),
        ]

        grid = QGridLayout()
        grid.setSpacing(12)

        for index, (label, target) in enumerate(quick_access_items):
            button = QPushButton(label)
            button.setObjectName("action_button")
            button.setMinimumHeight(60)
            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            button.clicked.connect(
                lambda checked=False, page=target: self.show_page(page)
            )

            grid.addWidget(button, index // 2, index % 2)

        layout.addLayout(grid)

        welcome_panel = QFrame()
        welcome_panel.setObjectName("panel")

        welcome_layout = QVBoxLayout(welcome_panel)
        welcome_layout.setContentsMargins(18, 16, 18, 16)
        welcome_layout.setSpacing(8)

        welcome_title = QLabel("Welcome to Utility Hub")
        welcome_title.setObjectName("panel_title")

        welcome_text = QLabel(
            "Your personal workspace for system monitoring, "
            "applications, scripts, cybersecurity tools, and projects."
        )
        welcome_text.setObjectName("muted_text")
        welcome_text.setWordWrap(True)

        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_text)

        layout.addSpacing(15)
        layout.addWidget(welcome_panel)

    def build_system_page(self, layout):
        """Build the live system monitoring dashboard."""

        refresh_row = QHBoxLayout()

        update_status = QLabel(
            "Live monitoring • Updates every second"
        )
        update_status.setObjectName("muted_text")

        refresh_row.addWidget(update_status)
        refresh_row.addStretch()

        refresh_button = QPushButton("Refresh")
        refresh_button.setObjectName("action_button")
        refresh_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        refresh_button.clicked.connect(self.refresh_system_info)

        refresh_row.addWidget(refresh_button)
        layout.addLayout(refresh_row)

        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(12)

        self.add_metric_card(
            metrics_grid,
            0,
            0,
            "CPU Usage",
            "cpu_usage",
        )

        self.add_metric_card(
            metrics_grid,
            0,
            1,
            "Memory Usage",
            "ram_usage",
        )

        self.add_metric_card(
            metrics_grid,
            1,
            0,
            "Disk Usage",
            "disk_usage",
        )

        self.add_metric_card(
            metrics_grid,
            1,
            1,
            "System Uptime",
            "uptime",
        )

        layout.addLayout(metrics_grid)

        details_panel = QFrame()
        details_panel.setObjectName("panel")

        details_layout = QVBoxLayout(details_panel)
        details_layout.setContentsMargins(18, 16, 18, 16)
        details_layout.setSpacing(10)

        details_title = QLabel("System Details")
        details_title.setObjectName("panel_title")

        details_layout.addWidget(details_title)

        detail_fields = [
            ("Computer Name", "computer_name"),
            ("Operating System", "operating_system"),
            ("OS Version", "os_version"),
            ("Processor", "processor"),
            ("Logical Cores", "logical_cores"),
            ("Architecture", "architecture"),
            ("Python Version", "python_version"),
            ("Memory", "ram_details"),
            ("Disk", "disk_details"),
        ]

        for label_text, key in detail_fields:
            row = QHBoxLayout()

            field_label = QLabel(label_text)
            field_label.setObjectName("muted_text")

            value_label = QLabel("Loading...")
            value_label.setWordWrap(True)
            value_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )

            row.addWidget(field_label, 1)
            row.addWidget(value_label, 2)

            details_layout.addLayout(row)

            self.system_labels[key] = value_label

        layout.addWidget(details_panel)

    def add_metric_card(self, grid, row, column, title, key):
        """Create a reusable system metric card."""

        panel = QFrame()
        panel.setObjectName("panel")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 14, 16, 14)
        panel_layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("panel_title")

        value_label = QLabel("Loading...")
        value_label.setObjectName("metric_value")
        value_label.setMinimumHeight(32)

        panel_layout.addWidget(title_label)
        panel_layout.addWidget(value_label)

        if key in ("cpu_usage", "ram_usage", "disk_usage"):
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(0)
            progress_bar.setTextVisible(False)

            panel_layout.addWidget(progress_bar)

            self.system_progress_bars[key] = progress_bar

        grid.addWidget(panel, row, column)

        self.system_labels[key] = value_label

    def build_placeholder_page(self, layout, page_name):
        """Build a placeholder for a page not yet implemented."""

        panel = QFrame()
        panel.setObjectName("panel")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(18, 16, 18, 16)

        message = QLabel(
            f"The {page_name} page is ready for future features."
        )
        message.setObjectName("muted_text")
        message.setWordWrap(True)

        panel_layout.addWidget(message)
        layout.addWidget(panel)

    def refresh_system_info(self):
        """Refresh system metrics and details."""

        info = get_system_info()

        # CPU usage
        cpu_usage = info["cpu_usage"]

        self.system_labels["cpu_usage"].setText(
            f"{cpu_usage:.1f}%"
        )
        self.system_progress_bars["cpu_usage"].setValue(
            round(cpu_usage)
        )

        # Memory usage
        ram_usage = info["ram_usage"]

        self.system_labels["ram_usage"].setText(
            f"{ram_usage:.1f}%"
        )
        self.system_progress_bars["ram_usage"].setValue(
            round(ram_usage)
        )

        # Disk usage
        disk_usage = info["disk_usage"]

        self.system_labels["disk_usage"].setText(
            f"{disk_usage:.1f}%"
        )
        self.system_progress_bars["disk_usage"].setValue(
            round(disk_usage)
        )

        # System uptime
        self.system_labels["uptime"].setText(
            info["uptime"]
        )

        # System details
        detail_values = {
            "computer_name": info["computer_name"],
            "operating_system": info["operating_system"],
            "os_version": info["os_version"],
            "processor": info["processor"],
            "logical_cores": str(info["logical_cores"]),
            "architecture": info["architecture"],
            "python_version": info["python_version"],
            "ram_details": (
                f'{info["ram_used_gb"]} GB used / '
                f'{info["ram_total_gb"]} GB total'
            ),
            "disk_details": (
                f'{info["disk_used_gb"]} GB used / '
                f'{info["disk_total_gb"]} GB total'
            ),
        }

        for key, value in detail_values.items():
            self.system_labels[key].setText(value)

    def show_page(self, page_name):
        """Display a page and update the active navigation button."""

        page = self.pages[page_name]
        self.page_stack.setCurrentWidget(page)

        for name, button in self.navigation_buttons.items():
            button.setChecked(name == page_name)