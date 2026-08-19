"""The Construct: detect and explain Python virtual environments."""
import os
import site
import sys


def in_virtual_env() -> bool:
    """Tell whether the interpreter runs inside a virtual environment."""
    return sys.prefix != sys.base_prefix


def show_construct() -> None:
    """Display details about the active virtual environment."""
    print()
    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Environment Path: {sys.prefix}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    for path in site.getsitepackages():
        print(path)


def show_plugged_in() -> None:
    """Warn about the global environment and give venv instructions."""
    print()
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("Global package installation path:")
    for path in site.getsitepackages():
        print(path)
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate  # On Windows")
    print()
    print("Then run this program again.")


def main() -> None:
    """Report the current environment status."""
    try:
        if in_virtual_env():
            show_construct()
        else:
            show_plugged_in()
    except Exception as exc:
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
