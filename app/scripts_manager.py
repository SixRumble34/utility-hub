import ast
import sys
from pathlib import Path

from PySide6.QtCore import QObject, QProcess, QTimer, Signal


class ScriptManager(QObject):
    output_received = Signal(str)
    error_received = Signal(str)
    process_finished = Signal(int, bool)
    running_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project_root = Path(__file__).resolve().parent.parent
        self.scripts_directory = self.project_root / "scripts"
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
        self.process.errorOccurred.connect(self.handle_process_error)

    def discover_scripts(self):
        """Find Python scripts directly inside the scripts directory."""

        self.scripts_directory.mkdir(parents=True, exist_ok=True)

        discovered_scripts = []

        for script_path in sorted(
            self.scripts_directory.glob("*.py"),
            key=lambda path: path.name.lower(),
        ):
            if script_path.name.startswith("_"):
                continue

            discovered_scripts.append(
                {
                    "name": script_path.stem.replace("_", " ").title(),
                    "filename": script_path.name,
                    "path": script_path,
                    "description": self.get_description(script_path),
                }
            )

        return discovered_scripts

    def get_description(self, script_path):
        """Read a script's docstring without executing the script."""

        try:
            source = script_path.read_text(encoding="utf-8")
            syntax_tree = ast.parse(source, filename=script_path.name)
            description = ast.get_docstring(syntax_tree)

            if description:
                return description.splitlines()[0]

            return "Python script"

        except (OSError, SyntaxError, UnicodeDecodeError):
            return "Unable to read script description"

    def is_running(self):
        return (
            self.process.state()
            != QProcess.ProcessState.NotRunning
        )

    def run_script(self, script_path):
        """Run a selected Python script in a separate process."""

        if self.is_running():
            return False

        script_path = Path(script_path).resolve()
        scripts_root = self.scripts_directory.resolve()

        try:
            script_path.relative_to(scripts_root)
        except ValueError:
            self.error_received.emit(
                "Error: The selected script is outside the scripts folder."
            )
            return False

        if not script_path.is_file() or script_path.suffix.lower() != ".py":
            self.error_received.emit(
                "Error: The selected Python script does not exist."
            )
            return False

        self.stop_requested = False

        self.process.setWorkingDirectory(str(self.project_root))
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

    def read_standard_output(self):
        output = bytes(
            self.process.readAllStandardOutput()
        ).decode("utf-8", errors="replace")

        if output:
            self.output_received.emit(output)

    def read_standard_error(self):
        error_output = bytes(
            self.process.readAllStandardError()
        ).decode("utf-8", errors="replace")

        if error_output:
            self.error_received.emit(error_output)

    def handle_started(self):
        self.running_changed.emit(True)

    def handle_finished(self, exit_code, exit_status):
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
        if error == QProcess.ProcessError.FailedToStart:
            self.stop_timer.stop()

            self.error_received.emit(
                "Error: Python could not start the selected script."
            )

            self.running_changed.emit(False)