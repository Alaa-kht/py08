"""Loading Programs: package management with pip and Poetry."""
import importlib
import sys
from typing import Any

PROGRAMS: list[tuple[str, str]] = [
    ("pandas", "Data manipulation ready"),
    ("numpy", "Numerical computation ready"),
    ("matplotlib", "Visualization ready"),
]


def load_program(name: str) -> Any:
    """Import a package by name; return None if it is missing."""
    try:
        return importlib.import_module(name)
    except ImportError:
        return None


def check_dependencies() -> dict[str, Any]:
    """Compare installed package versions against the needed ones."""
    print("Checking dependencies:")
    loaded: dict[str, Any] = {}
    for name, role in PROGRAMS:
        module = load_program(name)
        if module is None:
            print(f"[MISSING] {name} - not installed")
        else:
            version = getattr(module, "__version__", "unknown")
            print(f"[OK] {name} ({version}) - {role}")
            loaded[name] = module
    return loaded


def show_install_instructions() -> None:
    """Explain how to install the missing programs."""
    print()
    print("Some programs are missing. Load them with:")
    print()
    print("With pip (reads requirements.txt):")
    print("  python -m venv matrix_env")
    print("  source matrix_env/bin/activate")
    print("  pip install -r requirements.txt")
    print()
    print("With Poetry (reads pyproject.toml):")
    print("  poetry install")
    print("  poetry run python loading.py")


def show_pip_vs_poetry() -> None:
    """Show the differences between pip and Poetry."""
    print()
    print("pip vs Poetry:")
    print("pip: installs from requirements.txt into the active")
    print("     environment; versions pinned by hand; no lock file")
    print("     by default.")
    print("Poetry: reads pyproject.toml, resolves compatible versions,")
    print("     writes poetry.lock for reproducible installs and")
    print("     manages the virtual environment itself.")


def analyze(loaded: dict[str, Any]) -> None:
    """Generate Matrix data with numpy, analyze it, plot it."""
    np = loaded["numpy"]
    pd = loaded["pandas"]
    mpl = loaded["matplotlib"]
    mpl.use("Agg")
    plt = importlib.import_module("matplotlib.pyplot")
    print()
    print("Analyzing Matrix data...")
    rng = np.random.default_rng(42)
    signal = rng.normal(0.0, 1.0, 1000)
    frame = pd.DataFrame({"signal": signal})
    frame["smoothed"] = frame["signal"].rolling(20).mean()
    print(f"Processing {len(frame)} data points...")
    print("Generating visualization...")
    figure = plt.figure(figsize=(8, 4))
    plt.plot(frame.index, frame["signal"], alpha=0.4, label="signal")
    plt.plot(frame.index, frame["smoothed"], label="smoothed")
    plt.title("Matrix data stream")
    plt.legend()
    figure.savefig("matrix_analysis.png")
    plt.close(figure)
    print()
    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


def main() -> None:
    """Run the loading scenario."""
    try:
        print()
        print("LOADING STATUS: Loading programs...")
        print()
        loaded = check_dependencies()
        show_pip_vs_poetry()
        if len(loaded) < len(PROGRAMS):
            show_install_instructions()
            sys.exit(0)
        analyze(loaded)
    except Exception as exc:
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
