import unittest
from unittest.mock import MagicMock, patch

from app.notifications import DesktopNotifications


class TestDesktopNotifications(unittest.TestCase):
    @patch("app.notifications.QSystemTrayIcon.isSystemTrayAvailable")
    @patch("app.notifications.QSystemTrayIcon")
    @patch("app.notifications.QApplication.instance")
    def test_notification_uses_requested_duration(
        self,
        mock_app_instance,
        mock_tray_class,
        mock_tray_available,
    ):
        mock_tray_available.return_value = True

        mock_app = MagicMock()
        mock_app.style.return_value.standardIcon.return_value = MagicMock()
        mock_app_instance.return_value = mock_app

        mock_tray = mock_tray_class.return_value
        mock_tray.isVisible.return_value = True

        notifications = DesktopNotifications()
        result = notifications.notify(
            "Test Notification",
            "Testing notification duration.",
            duration=5000,
        )

        self.assertTrue(result)
        mock_tray.showMessage.assert_called_once_with(
            "Test Notification",
            "Testing notification duration.",
            mock_tray_class.MessageIcon.Information,
            5000,
        )

    @patch("app.notifications.QSystemTrayIcon.isSystemTrayAvailable")
    def test_notification_returns_false_when_tray_unavailable(
        self,
        mock_tray_available,
    ):
        mock_tray_available.return_value = False

        notifications = DesktopNotifications()
        result = notifications.notify(
            "Test Notification",
            "The tray is unavailable.",
        )

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()