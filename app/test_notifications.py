from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QStyle,
    QSystemTrayIcon,
)

app = QApplication([])

print("System tray available:", QSystemTrayIcon.isSystemTrayAvailable())
print("System tray supports messages:", QSystemTrayIcon.supportsMessages())

tray = QSystemTrayIcon(app.style().standardIcon(
    QStyle.StandardPixmap.SP_ComputerIcon
))
tray.setToolTip("Utility Hub Notification Test")
tray.show()

def send_test_notification():
    print("Sending test notification...")
    tray.showMessage(
        "Utility Hub Test",
        "If you can see this, desktop notifications are working.",
        QSystemTrayIcon.MessageIcon.Information,
        5000,
    )

    QTimer.singleShot(7000, app.quit)

QTimer.singleShot(1000, send_test_notification)

app.exec()