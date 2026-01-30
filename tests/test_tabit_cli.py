"""E2E tests for tabit-cli."""

import pytest


class TestTabitCliHelp:
    """Test --help flag."""

    def test_help_shows_usage(self, run_tabit):
        """--help should show usage information."""
        result = run_tabit(["--help"])
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower() or "Usage:" in result.stdout
        assert "--date" in result.stdout
        assert "--time" in result.stdout
        assert "--restaurant" in result.stdout
        assert "--batch" in result.stdout


class TestTabitCliValidation:
    """Test input validation."""

    def test_invalid_date_format(self, run_tabit):
        """Invalid date format should error."""
        result = run_tabit(["--restaurant", "DOK", "--date", "2026-01-31"])
        assert result.returncode == 1
        assert "Invalid date format" in result.stdout or "Invalid date" in result.stderr

    def test_invalid_time_format(self, run_tabit):
        """Invalid time format should error."""
        result = run_tabit(["--restaurant", "DOK", "--date", "20260201", "--time", "19:00"])
        assert result.returncode == 1
        assert "Invalid time format" in result.stdout or "Invalid time" in result.stderr

    def test_unknown_restaurant(self, run_tabit, tomorrow_date):
        """Unknown restaurant name should error gracefully."""
        result = run_tabit(["--restaurant", "NonExistentRestaurant12345", "--date", tomorrow_date])
        assert result.returncode == 1
        assert "No Tabit restaurant matching" in result.stdout or "not found" in result.stdout.lower()

    def test_no_args_error(self, run_tabit):
        """Running without args should show error."""
        result = run_tabit([])
        assert result.returncode == 1
        assert "specify" in result.stdout.lower() or "--restaurant" in result.stdout


class TestTabitCliList:
    """Test --list flag."""

    def test_list_shows_restaurants(self, run_tabit):
        """--list should show restaurants from CSV."""
        result = run_tabit(["--list"])
        assert result.returncode == 0
        assert "DOK" in result.stdout
        assert "Habasta" in result.stdout


@pytest.mark.live_api
class TestTabitCliSingleRestaurant:
    """Test single restaurant search (hits real API)."""

    def test_search_by_name(self, run_tabit, tomorrow_date):
        """Search by restaurant name should return results or graceful error."""
        result = run_tabit([
            "--restaurant", "DOK",
            "--date", tomorrow_date,
            "--time", "1900",
        ])
        # Success OR graceful API response
        assert result.returncode == 0 or "Error" in result.stdout

    def test_search_by_id(self, run_tabit, tomorrow_date, sample_tabit_id):
        """Search by Tabit org ID should return results."""
        result = run_tabit([
            "--restaurant", sample_tabit_id,
            "--date", tomorrow_date,
            "--time", "1900",
        ])
        assert result.returncode == 0 or "Error" in result.stdout

    def test_raw_json_output(self, run_tabit, tomorrow_date, sample_tabit_id, parse_json):
        """--raw should output valid JSON."""
        result = run_tabit([
            "--restaurant", sample_tabit_id,
            "--date", tomorrow_date,
            "--time", "1900",
            "--raw",
        ])
        if result.returncode == 0:
            data = parse_json(result.stdout)
            assert isinstance(data, dict)

    def test_party_size_4(self, run_tabit, tomorrow_date):
        """Search with party size 4 should work."""
        result = run_tabit([
            "--restaurant", "DOK",
            "--date", tomorrow_date,
            "--time", "1900",
            "--people", "4",
        ])
        # Should not crash
        assert result.returncode == 0 or "Error" in result.stdout


@pytest.mark.live_api
@pytest.mark.slow
class TestTabitCliBatchMode:
    """Test batch mode (hits real API, slower)."""

    @pytest.mark.timeout(60)
    def test_batch_runs(self, run_tabit, tomorrow_date):
        """Batch mode should run and output results."""
        result = run_tabit([
            "--batch",
            "--date", tomorrow_date,
            "--time", "1900",
        ], timeout=60)
        # Batch should complete
        assert result.returncode == 0
        assert "Batch check:" in result.stdout or "restaurant" in result.stdout.lower()

    @pytest.mark.timeout(60)
    def test_batch_raw_json(self, run_tabit, tomorrow_date, parse_json):
        """Batch mode with --raw should output JSON array."""
        result = run_tabit([
            "--batch",
            "--date", tomorrow_date,
            "--time", "1900",
            "--raw",
        ], timeout=60)
        if result.returncode == 0:
            # Raw output includes progress lines before JSON
            # Find the JSON array in the output (first [ to last ])
            from conftest import strip_ansi
            stdout = strip_ansi(result.stdout)
            json_start = stdout.find("\n[")  # JSON array starts on new line
            if json_start >= 0:
                json_end = stdout.rfind("]") + 1
                if json_end > json_start:
                    data = parse_json(stdout[json_start:json_end])
                    assert isinstance(data, list)
