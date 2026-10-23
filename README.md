# Utility Hub

A personal Windows desktop utility launcher built with Python and PySide6. Utility Hub brings system monitoring, script execution, and quick-access tools together in one desktop application.

## Features

### System Overview
- Live CPU usage monitoring
- Memory and disk usage monitoring
- System uptime and hardware/software details

### Python Script Runner
- Automatically discovers Python scripts in the `scripts/` directory
- Search and select scripts from the application
- Run scripts in separate processes
- View standard output and error output
- Stop running scripts
- Display script execution status

### Desktop Notifications
- Notifications when scripts start
- Notifications when scripts complete successfully
- Notifications when scripts fail or stop
- Notifications when a script cannot start

### Application Interface
- Dark-themed desktop interface
- Sidebar navigation
- Home page with quick-access shortcuts
- Dedicated System and Scripts pages

## Requirements

- Windows
- Python 3.10 or newer
- PySide6
- psutil

## Installation

Clone the repository:

```powershell
git clone https://github.com/SixRumble34/utility-hub.git
cd utility-hub
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Running Utility Hub

From the project directory, run:

```powershell
python main.py
```

## Adding Scripts

Place your Python scripts directly inside the `scripts/` directory.

Utility Hub discovers Python files in that directory and allows you to run them through the Scripts page.

Only run scripts you trust. Scripts execute as separate processes with the permissions of your Windows account.

## Project Structure

```text
utility-hub/
├── app/
│   ├── main_window.py
│   ├── notifications.py
│   ├── scripts_manager.py
│   ├── style.py
│   └── system_info.py
├── scripts/
├── tests/
├── main.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Development

Utility Hub is under active development. Features and interface elements may change as the project evolves.

## License

See [LICENSE](LICENSE) for license details.
