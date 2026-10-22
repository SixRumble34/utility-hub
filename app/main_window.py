from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.scripts_manager import ScriptManager
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

        self.script_manager = ScriptManager(self)
        self.script_entries = []

        self.script_manager.output_received.connect(
            self.append_script_output
        )
        self.script_manager.error_received.connect(
            self.append_script_error
        )
        self.script_manager.process_finished.connect(
            self.handle_script_finished
        )
        self.script_manager.running_changed.connect(
            self.handle_script_running_changed
        )

        self.build_interface()

        self.refresh_system_info()

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
        """Build a page header and its content."""

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
                "Discover, run, and monitor your Python scripts."
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

        elif page_name == "Scripts":
            self.build_scripts_page(layout)

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
            metrics_grid, 0, 0, "CPU Usage", "cpu_usage"
        )
        self.add_metric_card(
            metrics_grid, 0, 1, "Memory Usage", "ram_usage"
        )
        self.add_metric_card(
            metrics_grid, 1, 0, "Disk Usage", "disk_usage"
        )
        self.add_metric_card(
            metrics_grid, 1, 1, "System Uptime", "uptime"
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

    def build_scripts_page(self, layout):
        """Build the script library and execution interface."""

        library_panel = QFrame()
        library_panel.setObjectName("panel")

        library_layout = QVBoxLayout(library_panel)
        library_layout.setContentsMargins(16, 16, 16, 16)
        library_layout.setSpacing(10)

        library_title = QLabel("Script Library")
        library_title.setObjectName("panel_title")
        library_layout.addWidget(library_title)

        self.script_search = QLineEdit()
        self.script_search.setObjectName("script_search")
        self.script_search.setPlaceholderText("Search scripts...")
        self.script_search.textChanged.connect(self.filter_scripts)
        library_layout.addWidget(self.script_search)

        self.script_list = QListWidget()
        self.script_list.setMinimumHeight(100)
        self.script_list.currentItemChanged.connect(
            self.select_script
        )
        library_layout.addWidget(self.script_list, 1)

        library_buttons = QHBoxLayout()

        refresh_button = QPushButton("Refresh Library")
        refresh_button.setObjectName("secondary_button")
        refresh_button.clicked.connect(self.refresh_script_library)

        library_buttons.addWidget(refresh_button)
        library_buttons.addStretch()

        library_layout.addLayout(library_buttons)
        layout.addWidget(library_panel, 2)

        details_panel = QFrame()
        details_panel.setObjectName("panel")

        details_layout = QVBoxLayout(details_panel)
        details_layout.setContentsMargins(16, 16, 16, 16)
        details_layout.setSpacing(8)

        details_title = QLabel("Script Details")
        details_title.setObjectName("panel_title")
        details_layout.addWidget(details_title)

        self.selected_script_label = QLabel("No script selected")
        self.selected_script_label.setObjectName("panel_title")
        self.selected_script_label.setWordWrap(True)
        details_layout.addWidget(self.selected_script_label)

        self.script_path_label = QLabel(
            "Select a script to see its location."
        )
        self.script_path_label.setObjectName("muted_text")
        self.script_path_label.setWordWrap(True)
        details_layout.addWidget(self.script_path_label)

        self.script_description_label = QLabel(
            "Choose a script from the library."
        )
        self.script_description_label.setObjectName("muted_text")
        self.script_description_label.setWordWrap(True)
        details_layout.addWidget(self.script_description_label)

        controls = QHBoxLayout()

        self.run_script_button = QPushButton("Run Script")
        self.run_script_button.setObjectName("action_button")
        self.run_script_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.run_script_button.clicked.connect(self.run_selected_script)

        self.stop_script_button = QPushButton("Stop Script")
        self.stop_script_button.setObjectName("danger_button")
        self.stop_script_button.setEnabled(False)
        self.stop_script_button.clicked.connect(
            self.stop_selected_script
        )

        controls.addWidget(self.run_script_button)
        controls.addWidget(self.stop_script_button)
        controls.addStretch()

        details_layout.addLayout(controls)

        self.script_status_label = QLabel("Ready")
        self.script_status_label.setObjectName("status_text")
        details_layout.addWidget(self.script_status_label)

        output_title = QLabel("Execution Output")
        output_title.setObjectName("panel_title")
        details_layout.addWidget(output_title)

        self.script_output = QPlainTextEdit()
        self.script_output.setObjectName("script_output")
        self.script_output.setReadOnly(True)
        self.script_output.setPlaceholderText(
            "Script output and errors will appear here."
        )
        self.script_output.setMinimumHeight(100)
        details_layout.addWidget(self.script_output, 1)

        output_buttons = QHBoxLayout()

        clear_output_button = QPushButton("Clear Output")
        clear_output_button.setObjectName("secondary_button")
        clear_output_button.clicked.connect(self.script_output.clear)

        output_buttons.addWidget(clear_output_button)
        output_buttons.addStretch()

        details_layout.addLayout(output_buttons)
        layout.addWidget(details_panel, 3)

        self.refresh_script_library()

    def refresh_script_library(self):
        """Reload scripts from the scripts directory."""

        selected_path = None
        current_item = self.script_list.currentItem()

        if current_item is not None:
            selected_path = current_item.data(
                Qt.ItemDataRole.UserRole
            )

        self.script_list.clear()
        self.script_entries = self.script_manager.discover_scripts()

        for script in self.script_entries:
            item = QListWidgetItem(script["name"])
            item.setData(
                Qt.ItemDataRole.UserRole,
                str(script["path"]),
            )
            item.setToolTip(script["filename"])
            self.script_list.addItem(item)

            if str(script["path"]) == selected_path:
                self.script_list.setCurrentItem(item)

        if self.script_list.count() == 0:
            self.selected_script_label.setText("No scripts found")
            self.script_path_label.setText(
                "Add Python files to the project's scripts folder."
            )
            self.script_description_label.setText(
                "Python files directly inside scripts/ are discovered."
            )
            self.run_script_button.setEnabled(False)

        elif self.script_list.currentItem() is None:
            self.script_list.setCurrentRow(0)

        self.filter_scripts(self.script_search.text())

    def filter_scripts(self, search_text):
        """Filter visible scripts by name or filename."""

        search_text = search_text.strip().lower()

        for index in range(self.script_list.count()):
            item = self.script_list.item(index)
            name = item.text().lower()
            filename = item.toolTip().lower()

            item.setHidden(
                search_text not in name
                and search_text not in filename
            )

        current_item = self.script_list.currentItem()

        if current_item is not None and current_item.isHidden():
            self.script_list.setCurrentItem(None)

        if self.script_list.currentItem() is None:
            for index in range(self.script_list.count()):
                item = self.script_list.item(index)

                if not item.isHidden():
                    self.script_list.setCurrentItem(item)
                    break

    def select_script(self, current_item, previous_item=None):
        """Display details for the selected script."""

        if current_item is None:
            self.selected_script_label.setText("No script selected")
            self.script_path_label.setText(
                "Select a script from the library."
            )
            self.script_description_label.setText("")
            self.run_script_button.setEnabled(
                not self.script_manager.is_running()
            )
            return

        script_path = current_item.data(Qt.ItemDataRole.UserRole)

        script = next(
            (
                entry
                for entry in self.script_entries
                if str(entry["path"]) == script_path
            ),
            None,
        )

        if script is None:
            return

        self.selected_script_label.setText(script["filename"])
        self.script_path_label.setText(str(script["path"]))
        self.script_description_label.setText(script["description"])

        self.run_script_button.setEnabled(
            not self.script_manager.is_running()
        )

    def run_selected_script(self):
        """Run the currently selected script."""

        if self.script_manager.is_running():
            return

        item = self.script_list.currentItem()

        if item is None:
            QMessageBox.information(
                self,
                "No Script Selected",
                "Select a script before choosing Run Script.",
            )
            return

        script_path = item.data(Qt.ItemDataRole.UserRole)

        self.script_output.clear()
        self.script_status_label.setText("Starting script...")

        self.run_script_button.setEnabled(False)
        self.stop_script_button.setEnabled(False)

        started = self.script_manager.run_script(script_path)

        if not started:
            self.script_status_label.setText(
                "Unable to start script."
            )
            self.run_script_button.setEnabled(True)

    def stop_selected_script(self):
        """Request the running script to stop."""

        if self.script_manager.is_running():
            self.script_status_label.setText(
                "Requesting script to stop..."
            )
            self.stop_script_button.setEnabled(False)
            self.script_manager.stop_script()

    def append_script_output(self, output):
        """Append standard output from a running script."""

        cursor = self.script_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.script_output.setTextCursor(cursor)
        self.script_output.insertPlainText(output)
        self.script_output.ensureCursorVisible()

    def append_script_error(self, error_output):
        """Append standard error from a running script."""

        cursor = self.script_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.script_output.setTextCursor(cursor)
        self.script_output.insertPlainText(error_output)
        self.script_output.ensureCursorVisible()

    def handle_script_running_changed(self, is_running):
        """Update execution controls when the process state changes."""

        self.run_script_button.setEnabled(
            not is_running
            and self.script_list.currentItem() is not None
        )
        self.stop_script_button.setEnabled(is_running)

        if is_running:
            self.script_status_label.setText("Running...")

    def handle_script_finished(self, exit_code, succeeded):
        """Display the final execution result."""

        if succeeded:
            self.script_status_label.setText(
                f"Completed successfully (exit code {exit_code})."
            )
            self.script_output.appendPlainText(
                f"\n[Utility Hub] Script completed with exit code {exit_code}."
            )
        else:
            self.script_status_label.setText(
                f"Failed or stopped (exit code {exit_code})."
            )
            self.script_output.appendPlainText(
                f"\n[Utility Hub] Script exited with code {exit_code}."
            )

        self.run_script_button.setEnabled(
            self.script_list.currentItem() is not None
        )
        self.stop_script_button.setEnabled(False)

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

        cpu_usage = info["cpu_usage"]
        self.system_labels["cpu_usage"].setText(f"{cpu_usage:.1f}%")
        self.system_progress_bars["cpu_usage"].setValue(round(cpu_usage))

        ram_usage = info["ram_usage"]
        self.system_labels["ram_usage"].setText(f"{ram_usage:.1f}%")
        self.system_progress_bars["ram_usage"].setValue(round(ram_usage))

        disk_usage = info["disk_usage"]
        self.system_labels["disk_usage"].setText(f"{disk_usage:.1f}%")
        self.system_progress_bars["disk_usage"].setValue(round(disk_usage))

        self.system_labels["uptime"].setText(info["uptime"])

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