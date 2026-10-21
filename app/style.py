
APP_STYLESHEET = """
QMainWindow {
    background-color: #171D28;
}

QWidget {
    color: #E7ECF3;
    font-family: "Segoe UI";
    font-size: 10pt;
}

QWidget#Sidebar {
    background-color: #202936;
    border-right: 1px solid #343C4A;
}

QWidget#MainContent {
    background-color: #171D28;
}

QLabel#AppTitle {
    font-size: 16pt;
    font-weight: 700;
    color: #F1F5F9;
}

QLabel#SectionLabel {
    color: #8F9BAD;
    font-size: 8pt;
    font-weight: 600;
}

QLabel#PageTitle {
    font-size: 23pt;
    font-weight: 700;
    color: #F1F5F9;
}

QLabel#MutedText {
    color: #9BA8BA;
}

QLabel#ProfileAvatar {
    background-color: #365D96;
    color: #FFFFFF;
    border-radius: 20px;
    font-size: 13pt;
    font-weight: 700;
}

QPushButton {
    background-color: transparent;
    color: #B0BAC9;
    border: none;
    border-radius: 6px;
    padding: 10px;
    text-align: left;
}

QPushButton:hover {
    background-color: #2A3545;
    color: #FFFFFF;
}

QPushButton:checked {
    background-color: #304A6D;
    color: #FFFFFF;
    font-weight: 600;
}

QFrame#ContentCard {
    background-color: #232E3D;
    border: 1px solid #343F50;
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

QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollArea > QWidget > QWidget {
    background-color: transparent;
}
"""
