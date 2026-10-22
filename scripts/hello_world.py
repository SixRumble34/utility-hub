"""A simple test script for Utility Hub's script runner."""

import platform
import sys
from datetime import datetime


def main():
    print("Hello from Utility Hub!")
    print("=" * 35)
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Operating system: {platform.system()}")
    print(f"Computer name: {platform.node()}")
    print(
        f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print()
    print("Script completed successfully.")


if __name__ == "__main__":
    main()