APP_STYLESHEET = """
QMainWindow {
    background-color: #111827;
    color: #F9FAFB;
}

QWidget {
    color: #F9FAFB;
    font-family: "Segoe UI";
    font-size: 10pt;
}

/* Main application layout */

QFrame#sidebar {
    background-color: #0B1220;
    border: none;
}

QWidget#MainContent {
    background-color: #111827;
}

/* Headings and text */

QLabel#app_title {
    font-size: 17pt;
    font-weight: bold;
    color: #F9FAFB;
    padding: 8px;
}

QLabel#page_title {
    font-size: 23pt;
    font-weight: bold;
    color: #F9FAFB;
}

QLabel#page_description {
    color: #9CA3AF;
    font-size: 10pt;
}

QLabel#panel_title {
    font-size: 12pt;
    font-weight: bold;
    color: #F9FAFB;
}

QLabel#metric_value {
    font-size: 20pt;
    font-weight: bold;
    color: #60A5FA;
}

QLabel#muted_text {
    color: #9CA3AF;
}

QLabel#status_text {
    color: #9CA3AF;
    font-size: 9pt;
}

/* Sidebar navigation */

QPushButton#nav_button {
    background-color: transparent;
    color: #D1D5DB;
    text-align: left;
    border: none;
    border-radius: 7px;
    padding: 11px;
}

QPushButton#nav_button:hover {
    background-color: #1F2937;
}

QPushButton#nav_button:checked {
    background-color: #1D4ED8;
    color: #FFFFFF;
}

QPushButton#settings_button {
    background-color: #111827;
    color: #D1D5DB;
    border: 1px solid #374151;
    border-radius: 7px;
    padding: 10px;
}

QPushButton#settings_button:hover {
    background-color: #1F2937;
}

/* General buttons */

QPushButton#action_button {
    background-color: #1D4ED8;
    color: #FFFFFF;
    border: none;
    border-radius: 7px;
    padding: 10px 16px;
    font-weight: bold;
}

QPushButton#action_button:hover {
    background-color: #2563EB;
}

QPushButton#action_button:disabled {
    background-color: #374151;
    color: #9CA3AF;
}

QPushButton#secondary_button {
    background-color: #303E50;
    color: #F1F5F9;
    border: 1px solid #3A4A60;
    border-radius: 7px;
    padding: 10px 16px;
}

QPushButton#secondary_button:hover {
    background-color: #3A4D67;
    border-color: #547DBA;
}

QPushButton#danger_button {
    background-color: #991B1B;
    color: #FFFFFF;
    border: none;
    border-radius: 7px;
    padding: 10px 16px;
    font-weight: bold;
}

QPushButton#danger_button:hover {
    background-color: #B91C1C;
}

/* Cards and panels */

QFrame#panel {
    background-color: #1F2937;
    border: 1px solid #374151;
    border-radius: 10px;
}

QFrame#ContentCard {
    background-color: #1F2937;
    border: 1px solid #374151;
    border-radius: 10px;
}

QPushButton#QuickLaunchButton {
    background-color: #303E50;
    border: 1px solid #3A4A60;
    border-radius: 8px;
    padding: 14px;
    color: #F1F5F9;
    font-weight: 600;
}

QPushButton#QuickLaunchButton:hover {
    background-color: #3A4D67;
    border: 1px solid #547DBA;
}

/* System monitoring */

QProgressBar {
    background-color: #111827;
    border: none;
    border-radius: 4px;
    height: 9px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #3B82F6;
    border-radius: 4px;
}

/* Script output and execution status */

QPlainTextEdit#script_output {
    background-color: #0B1220;
    color: #D1D5DB;
    border: 1px solid #374151;
    border-radius: 7px;
    padding: 10px;
    font-family: Consolas;
    font-size: 10pt;
}

QLineEdit#script_search {
    background-color: #111827;
    color: #F9FAFB;
    border: 1px solid #374151;
    border-radius: 7px;
    padding: 9px;
}

QLineEdit#script_search:focus {
    border: 1px solid #3B82F6;
}

QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollArea > QWidget > QWidget {
    background-color: transparent;
}
"""