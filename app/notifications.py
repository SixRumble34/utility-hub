from PySide6.QtWidgets import (
    QApplication,
    QStyle,
    QSystemTrayIcon,
)


class DesktopNotifications:
    """Display desktop notifications for Utility Hub."""

    def __init__(self, parent=None):
        self.tray_icon = QSystemTrayIcon(parent)

        app = QApplication.instance()

        if app is not None:
            icon = app.style().standardIcon(
                QStyle.StandardPixmap.SP_ComputerIcon
            )
            self.tray_icon.setIcon(icon)

        self.tray_icon.setToolTip("Utility Hub")
        self.tray_icon.setVisible(
            QSystemTrayIcon.isSystemTrayAvailable()
        )

    def notify(self, title, message, duration=5000):
        """Request a desktop notification."""

        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("[Utility Hub] System tray is unavailable.")
            return False

        if not self.tray_icon.isVisible():
            self.tray_icon.show()

        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.MessageIcon.Information,
            duration,
        )

        print(f"[Utility Hub] Notification requested: {title}")
        return True