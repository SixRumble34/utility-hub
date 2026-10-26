import unittest
from unittest.mock import MagicMock, patch

import app.notifications as notifications_module


class FakeTrayIcon:
    class MessageIcon:
        Information = "Information"

    def __init__(self, parent=None):
        self.visible = False
        self.messages = []

    def setIcon(self, icon):
        pass

    def setToolTip(self, text):
        pass

    def setVisible(self, visible):
        self.visible = visible

    def isVisible(self):
        return self.visible

    def show(self):
        self.visible = True

    def showMessage(self, title, message, icon, duration):
        self.messages.append((title, message, icon, duration))


class TestDesktopNotifications(unittest.TestCase):
    def setUp(self):
        self.tray_patcher = patch.object(
            notifications_module,
            "QSystemTrayIcon",
            FakeTrayIcon,
        )
        self.app_patcher = patch.object(
            notifications_module,
            "QApplication",
        )
        self.style_patcher = patch.object(
            notifications_module,
            "QStyle",
        )

        self.tray_patcher.start()
        self.mock_app_class = self.app_patcher.start()
        self.style_patcher.start()

        self.addCleanup(self.style_patcher.stop)
        self.addCleanup(self.app_patcher.stop)
        self.addCleanup(self.tray_patcher.stop)

        self.mock_app = MagicMock()
        self.mock_app_class.instance.return_value = self.mock_app
        self.mock_app.style.return_value.standardIcon.return_value = (
            "test-icon"
        )

    def test_notification_uses_requested_duration(self):
        with patch.object(
            notifications_module.QSystemTrayIcon,
            "isSystemTrayAvailable",
            return_value=True,
            create=True,
        ):
            notifications = notifications_module.DesktopNotifications()
            result = notifications.notify(
                "Test Notification",
                "Testing notification duration.",
                duration=5000,
            )

        self.assertTrue(result)
        self.assertEqual(
            notifications.tray_icon.messages,
            [
                (
                    "Test Notification",
                    "Testing notification duration.",
                    FakeTrayIcon.MessageIcon.Information,
                    5000,
                )
            ],
        )

    def test_notification_returns_false_when_tray_unavailable(self):
        with patch.object(
            notifications_module.QSystemTrayIcon,
            "isSystemTrayAvailable",
            return_value=False,
            create=True,
        ):
            notifications = notifications_module.DesktopNotifications()
            result = notifications.notify(
                "Test Notification",
                "The tray is unavailable.",
            )

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()