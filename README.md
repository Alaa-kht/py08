*This project has been created as part of the 42 curriculum by aalkhati.*

# Python Module 08 — The Matrix (Data Engineering Setup)

Real-world data engineering tooling: virtual environments, package
management with pip and Poetry, and secure configuration through
environment variables and .env files.

## Project structure

```
py08/
├── README.md
├── ex0/
│   └── construct.py        # Virtual environment detector + instructions
├── ex1/
│   ├── loading.py          # Dependency-aware data analysis program
│   ├── requirements.txt    # pip dependency file
│   └── pyproject.toml      # Poetry dependency file
└── ex2/
    ├── oracle.py           # Environment/.env configuration system
    ├── .env.example        # Documented placeholder configuration
    └── .gitignore          # Keeps the real .env out of git
```

## How to run

```bash
# ex0 — run outside, then inside a virtual environment:
python3 ex0/construct.py
python3 -m venv matrix_env && source matrix_env/bin/activate
python3 ex0/construct.py

# ex1 — run without dependencies, then install and rerun:
python3 ex1/loading.py
pip install -r ex1/requirements.txt        # or: poetry install
python3 ex1/loading.py                     # creates matrix_analysis.png

# ex2 — three configuration scenarios:
python3 ex2/oracle.py                      # defaults + warnings
cp ex2/.env.example ex2/.env && python3 ex2/oracle.py
MATRIX_MODE=production API_KEY=secret123 python3 ex2/oracle.py
```

Requirements: Python 3.10+. The virtual environment itself is NOT
committed — it is recreated on demand (that is the point).

## The exercises

### ex0 — Entering the Matrix (virtual environments)

`construct.py` detects whether it runs inside a venv with a single
comparison: `sys.prefix != sys.base_prefix`. Outside a venv both
point to the system installation, so they are equal; inside, `prefix`
points to the venv folder while `base_prefix` still points to the
real Python. The program adapts its output to each case: inside, it
shows the interpreter path, the environment name/path, and the venv
`site-packages` (where pip installs land); outside, it warns, shows
the GLOBAL package path, and prints the exact commands to create and
activate a venv (Unix and Windows variants). Running it in both
states makes the global-vs-virtual package location difference
visible — which is the whole lesson: a venv is just a folder with its
own `python` and its own `site-packages`, giving every project
isolated dependencies instead of one shared global soup.

### ex1 — Loading Programs (pip vs Poetry)

`loading.py` needs pandas, numpy and matplotlib — but must survive
their absence. Instead of top-level imports (which crash with
ImportError and trip flake8/mypy on missing packages), every package
is loaded through `importlib.import_module(name)` inside try/except:
present → `[OK] name (version) - role` using `__version__`;
missing → `[MISSING]` plus installation instructions for BOTH
managers. That is the "mechanics to avoid those errors" the subject
hints at, and it keeps flake8 and mypy fully clean. With everything
installed, the pipeline runs: numpy's random generator produces the
Matrix dataset (the required data source — no hardcoded lists or
range()), pandas wraps it in a DataFrame with a rolling mean, and
matplotlib (Agg backend) saves `matrix_analysis.png`. The program's
output also states the pip/Poetry difference: pip installs from a
hand-pinned `requirements.txt` into whatever environment is active;
Poetry reads `pyproject.toml`, resolves compatible versions, freezes
them in `poetry.lock` for reproducible installs, and manages the venv
itself. Both dependency files are provided.

### ex2 — Accessing the Mainframe (environment configuration)

`oracle.py` handles five variables (MATRIX_MODE, DATABASE_URL,
API_KEY, LOG_LEVEL, ZION_ENDPOINT) with a strict precedence chain:
**real environment > .env file > code defaults**. python-dotenv's
`load_dotenv()` fills the environment from `.env` but does NOT
override variables that already exist — which is exactly why
`MATRIX_MODE=production API_KEY=secret123 python3 oracle.py` wins
over the file. Missing variables produce `[WARN]` lines and safe
defaults instead of crashes. The development/production difference is
visible in the output as required: development shows the full
database URL, a masked API key and DEBUG logging; production hides
the URL, masks harder and defaults to INFO. A security-check section
reports on hardcoded secrets, `.env` presence, and override
availability. dotenv itself is imported through importlib so the
program degrades gracefully if the library is missing.

## Code quality

```bash
flake8 .    # passes clean
mypy .      # passes clean — the importlib pattern avoids the
            # import errors the subject would otherwise tolerate
```

Tested in all the states the subject demands: inside AND outside a
virtual environment, with AND without dependencies installed, and
under all three ex2 configuration scenarios.

## Concepts covered

- **Virtual environments**: per-project isolation via a private
  interpreter + `site-packages`; detected by comparing `sys.prefix`
  with `sys.base_prefix`; activation just prepends the venv's `bin/`
  to PATH so `python` resolves there.
- **pip vs Poetry**: imperative installs from requirements.txt versus
  declarative dependencies with resolution, a lock file, and managed
  environments. Same goal — reproducible dependencies — different
  philosophy.
- **Graceful dependency degradation**: `importlib.import_module` in
  try/except turns a hard ImportError into a helpful message, and
  keeps static analysis clean.
- **Environment-based configuration**: code reads `os.getenv`, never
  hardcodes secrets; behavior switches between dev and prod with zero
  code changes, driven purely by configuration.
- **Secret hygiene**: `.env` is gitignored because anything committed
  lives in git history forever; `.env.example` IS committed as
  documentation of the expected variables with placeholders.

## Design choices worth noting

- The venv is never committed and `matrix_env/` is gitignored: it is
  machine-specific, heavy, and entirely recreatable from the
  dependency files — recreatability is the feature.
- `load_dotenv()` is called with its default (no override) precisely
  to implement the environment-beats-file precedence the subject
  tests in the third scenario.
- API keys are masked in every output (first characters + stars);
  production masks more aggressively than development.
- matplotlib uses the Agg backend so the plot renders to a file on
  headless machines (no display server needed during review).
