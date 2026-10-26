import ast
import json
import sys
from pathlib import Path

from PySide6.QtCore import QObject, QProcess, QTimer, Signal


class ScriptManager(QObject):
    output_received = Signal(str)
    error_received = Signal(str)
    process_finished = Signal(int, bool)
    running_changed = Signal(bool)
    start_failed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project_root = Path(__file__).resolve().parent.parent
        self.scripts_directory = self.project_root / "scripts"

        self.settings_directory = (
            Path.home() / ".utility-hub"
        )
        self.settings_file = (
            self.settings_directory / "script_folders.json"
        )

        self.script_folders = [self.scripts_directory]
        self.load_script_folders()

        self.stop_requested = False

        self.stop_timer = QTimer(self)
        self.stop_timer.setSingleShot(True)
        self.stop_timer.setInterval(2000)
        self.stop_timer.timeout.connect(self.force_stop_script)

        self.process = QProcess(self)
        self.process.setProcessChannelMode(
            QProcess.ProcessChannelMode.SeparateChannels
        )

        self.process.readyReadStandardOutput.connect(
            self.read_standard_output
        )
        self.process.readyReadStandardError.connect(
            self.read_standard_error
        )
        self.process.started.connect(self.handle_started)
        self.process.finished.connect(self.handle_finished)
        self.process.errorOccurred.connect(
            self.handle_process_error
        )

    # ---------------------------------------------------------
    # SCRIPT FOLDER MANAGEMENT
    # ---------------------------------------------------------

    def load_script_folders(self):
        """Load additional script folders from saved settings."""

        if not self.settings_file.is_file():
            return

        try:
            saved_folders = json.loads(
                self.settings_file.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError):
            self.error_received.emit(
                "Warning: Saved script folders could not be loaded."
            )
            return

        if not isinstance(saved_folders, list):
            self.error_received.emit(
                "Warning: Saved script folder settings are invalid."
            )
            return

        for folder in saved_folders:
            if not isinstance(folder, str):
                continue

            folder_path = Path(folder).expanduser()

            if folder_path.is_dir():
                self._add_folder_to_list(folder_path)

    def save_script_folders(self):
        """Save additional script folders for future sessions."""

        additional_folders = [
            str(folder)
            for folder in self.script_folders
            if folder != self.scripts_directory
        ]

        try:
            self.settings_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.settings_file.write_text(
                json.dumps(additional_folders, indent=4),
                encoding="utf-8",
            )
        except OSError as error:
            self.error_received.emit(
                f"Error saving script folders: {error}"
            )

    def _add_folder_to_list(self, folder_path):
        """Add a normalized folder if it is not already registered."""

        folder_path = Path(folder_path).expanduser().resolve()

        for existing_folder in self.script_folders:
            if folder_path == existing_folder.resolve():
                return False

        self.script_folders.append(folder_path)
        return True

    def add_script_folder(self, folder_path):
        """Register an existing folder as a script-library location."""

        if not folder_path:
            return False

        folder_path = Path(folder_path).expanduser()

        if not folder_path.is_dir():
            self.error_received.emit(
                "Error: The selected script folder does not exist."
            )
            return False

        added = self._add_folder_to_list(folder_path)

        if added:
            self.save_script_folders()

        return added

    def remove_script_folder(self, folder_path):
        """Remove an additional folder without deleting its contents."""

        if not folder_path:
            return False

        folder_path = Path(folder_path).expanduser().resolve()
        default_folder = self.scripts_directory.resolve()

        if folder_path == default_folder:
            self.error_received.emit(
                "The default project scripts folder cannot be removed."
            )
            return False

        for existing_folder in self.script_folders:
            if existing_folder.resolve() == folder_path:
                self.script_folders.remove(existing_folder)
                self.save_script_folders()
                return True

        return False

    def get_script_folders(self):
        """Return all registered script-library folders."""

        return list(self.script_folders)

    # ---------------------------------------------------------
    # SCRIPT DISCOVERY
    # ---------------------------------------------------------

    def discover_scripts(self):
        """Discover Python scripts in all registered folders."""

        self.scripts_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        discovered_scripts = []
        seen_paths = set()

        for folder in self.script_folders:
            if not folder.is_dir():
                continue

            try:
                script_paths = sorted(
                    folder.rglob("*.py"),
                    key=lambda path: str(path).lower(),
                )
            except OSError:
                continue

            for script_path in script_paths:
                if script_path.name.startswith("_"):
                    continue

                try:
                    resolved_path = script_path.resolve()
                except OSError:
                    continue

                path_key = str(resolved_path).casefold()

                if path_key in seen_paths:
                    continue

                seen_paths.add(path_key)

                discovered_scripts.append(
                    {
                        "name": script_path.stem.replace(
                            "_", " "
                        ).title(),
                        "filename": script_path.name,
                        "path": resolved_path,
                        "description": self.get_description(
                            resolved_path
                        ),
                    }
                )

        return sorted(
            discovered_scripts,
            key=lambda script: script["name"].casefold(),
        )

    def get_description(self, script_path):
        """Read a script's docstring without executing it."""

        try:
            source = script_path.read_text(encoding="utf-8")
            syntax_tree = ast.parse(
                source,
                filename=str(script_path),
            )
            description = ast.get_docstring(syntax_tree)

            if description:
                return description.splitlines()[0]

            return "Python script"

        except (
            OSError,
            SyntaxError,
            UnicodeDecodeError,
            ValueError,
        ):
            return "Unable to read script description"

    # ---------------------------------------------------------
    # SCRIPT EXECUTION
    # ---------------------------------------------------------

    def is_running(self):
        return (
            self.process.state()
            != QProcess.ProcessState.NotRunning
        )

    def run_script(self, script_path):
        """Run a selected Python script in a separate process."""

        if self.is_running():
            return False

        try:
            script_path = Path(script_path).expanduser().resolve()
        except (OSError, ValueError, TypeError):
            self.error_received.emit(
                "Error: The selected script path is invalid."
            )
            return False

        if (
            not script_path.is_file()
            or script_path.suffix.lower() != ".py"
        ):
            self.error_received.emit(
                "Error: The selected Python script does not exist."
            )
            return False

        # The script must belong to one of the registered folders.
        allowed = False

        for folder in self.script_folders:
            try:
                script_path.relative_to(folder.resolve())
                allowed = True
                break
            except ValueError:
                continue

        if not allowed:
            self.error_received.emit(
                "Error: The selected script is outside the "
                "registered script folders."
            )
            return False

        self.stop_requested = False

        # Use the script's own folder as its working directory.
        self.process.setWorkingDirectory(str(script_path.parent))
        self.process.setProgram(sys.executable)
        self.process.setArguments(["-u", str(script_path)])
        self.process.start()

        return True

    def stop_script(self):
        """Request termination, then force-stop after two seconds."""

        if not self.is_running():
            return

        self.stop_requested = True
        self.process.terminate()
        self.stop_timer.start()

    def force_stop_script(self):
        """Force-stop a process that did not terminate in time."""

        if self.is_running():
            self.process.kill()

    # ---------------------------------------------------------
    # PROCESS OUTPUT AND LIFECYCLE
    # ---------------------------------------------------------

    def read_standard_output(self):
        """Read standard output from the running process."""

        output = bytes(
            self.process.readAllStandardOutput()
        ).decode("utf-8", errors="replace")

        if output:
            self.output_received.emit(output)

    def read_standard_error(self):
        """Read standard error from the running process."""

        error_output = bytes(
            self.process.readAllStandardError()
        ).decode("utf-8", errors="replace")

        if error_output:
            self.error_received.emit(error_output)

    def handle_started(self):
        """Report that the script process has started."""

        self.running_changed.emit(True)

    def handle_finished(self, exit_code, exit_status):
        """Report the result when a script process finishes."""

        self.stop_timer.stop()

        self.read_standard_output()
        self.read_standard_error()

        succeeded = (
            not self.stop_requested
            and exit_code == 0
            and exit_status == QProcess.ExitStatus.NormalExit
        )

        self.process_finished.emit(exit_code, succeeded)
        self.running_changed.emit(False)

    def handle_process_error(self, error):
        """Handle errors raised by the process."""

        if error == QProcess.ProcessError.FailedToStart:
            self.stop_timer.stop()

            message = (
                "Error: Python could not start the selected script."
            )

            self.error_received.emit(message)
            self.start_failed.emit(message)
            self.running_changed.emit(False)