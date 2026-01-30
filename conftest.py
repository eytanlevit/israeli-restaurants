"""Shared pytest fixtures for E2E CLI tests."""

import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

# Project paths
PROJECT_ROOT = Path(__file__).parent.resolve()
ONTOPO_CLI = PROJECT_ROOT / "ontopo-cli"
TABIT_CLI = PROJECT_ROOT / "tabit-cli"
RESTAURANTS_CSV = PROJECT_ROOT / "restaurants.csv"

# Israel timezone for date calculations
ISRAEL_TZ = ZoneInfo("Asia/Jerusalem")


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def ontopo_cli_path() -> Path:
    """Return the path to ontopo-cli."""
    return ONTOPO_CLI


@pytest.fixture
def tabit_cli_path() -> Path:
    """Return the path to tabit-cli."""
    return TABIT_CLI


@pytest.fixture
def restaurants_csv_path() -> Path:
    """Return the path to restaurants.csv."""
    return RESTAURANTS_CSV


@pytest.fixture
def tomorrow_date() -> str:
    """Return tomorrow's date in YYYYMMDD format (Israel timezone)."""
    now = datetime.now(ISRAEL_TZ)
    return (now + timedelta(days=1)).strftime("%Y%m%d")


@pytest.fixture
def sample_ontopo_slug() -> str:
    """Sample OnTopo restaurant slug - Shila."""
    return "69127207"


@pytest.fixture
def sample_tabit_id() -> str:
    """Sample Tabit restaurant ID - DOK."""
    return "60ab7a96e463ba173196d5ce"


def run_cli(cli_path: Path, args: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
    """Execute a CLI script via uv run --script.

    Args:
        cli_path: Path to the CLI script (PEP 723 script with inline deps)
        args: Command line arguments

    Returns:
        CompletedProcess with stdout, stderr, returncode
    """
    # Use --script to tell uv this is a standalone script with inline dependencies
    # (not part of the project defined in pyproject.toml)
    cmd = ["uv", "run", "--script", str(cli_path)] + args
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=PROJECT_ROOT,
    )


@pytest.fixture
def run_ontopo(ontopo_cli_path):
    """Fixture that returns a function to run ontopo-cli."""
    def _run(args: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
        return run_cli(ontopo_cli_path, args, timeout)
    return _run


@pytest.fixture
def run_tabit(tabit_cli_path):
    """Fixture that returns a function to run tabit-cli."""
    def _run(args: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
        return run_cli(tabit_cli_path, args, timeout)
    return _run


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    ansi_pattern = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_pattern.sub('', text)


def parse_json_output(output: str) -> dict | list:
    """Parse JSON from CLI output, stripping ANSI codes first.

    Args:
        output: Raw CLI output that may contain ANSI codes

    Returns:
        Parsed JSON as dict or list
    """
    clean = strip_ansi(output)
    return json.loads(clean)


@pytest.fixture
def parse_json():
    """Fixture that returns the parse_json_output function."""
    return parse_json_output
