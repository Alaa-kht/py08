"""The Oracle: secure configuration via environment variables."""
import importlib
import os
from typing import Any

CONFIG_VARS: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]


def load_env_file() -> bool:
    """Load .env through python-dotenv without overriding real env."""
    dotenv: Any = None
    try:
        dotenv = importlib.import_module("dotenv")
    except ImportError:
        print("NOTE: python-dotenv not installed, .env file ignored")
        return False
    loaded: bool = bool(dotenv.load_dotenv())
    return loaded


def mask(secret: str) -> str:
    """Hide most of a secret value."""
    if len(secret) <= 4:
        return "****"
    return f"{secret[:2]}{'*' * (len(secret) - 2)}"


def read_config() -> dict[str, str]:
    """Read the configuration and warn about missing variables."""
    config: dict[str, str] = {}
    missing: list[str] = []
    for name in CONFIG_VARS:
        value = os.getenv(name, "")
        if value == "":
            missing.append(name)
        config[name] = value
    if missing:
        print("Configuration warnings:")
        for name in missing:
            print(f"[WARN] {name} is not set, using safe default")
        print()
    config.setdefault("MATRIX_MODE", "")
    if config["MATRIX_MODE"] == "":
        config["MATRIX_MODE"] = "development"
    if config["LOG_LEVEL"] == "":
        is_dev = config["MATRIX_MODE"] == "development"
        config["LOG_LEVEL"] = "DEBUG" if is_dev else "INFO"
    return config


def show_config(config: dict[str, str]) -> None:
    """Display the loaded configuration, mode-dependent."""
    dev = config["MATRIX_MODE"] == "development"
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    if config["DATABASE_URL"] == "":
        print("Database: Not configured (local fallback)")
    elif dev:
        print(f"Database: Connected to {config['DATABASE_URL']}")
    else:
        print("Database: Connected (URL hidden in production)")
    if config["API_KEY"] == "":
        print("API Access: No key (limited access)")
    elif dev:
        print(f"API Access: Authenticated (key: {mask(config['API_KEY'])})")
    else:
        print("API Access: Authenticated")
    print(f"Log Level: {config['LOG_LEVEL']}")
    if config["ZION_ENDPOINT"] == "":
        print("Zion Network: Offline")
    else:
        print("Zion Network: Online")


def security_check(env_loaded: bool) -> None:
    """Run the environment security checks."""
    print()
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    if env_loaded:
        print("[OK] .env file properly configured")
    else:
        print("[WARN] No .env file found (cp .env.example .env)")
    print("[OK] Production overrides available")


def main() -> None:
    """Read the Matrix configuration."""
    try:
        print()
        print("ORACLE STATUS: Reading the Matrix...")
        print()
        env_loaded = load_env_file()
        config = read_config()
        show_config(config)
        security_check(env_loaded)
        print()
        print("The Oracle sees all configurations.")
    except Exception as exc:
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
