"""E2E tests for ontopo-cli."""

import pytest


class TestOntopoCliHelp:
    """Test --help flag."""

    def test_help_shows_usage(self, run_ontopo):
        """--help should show usage information."""
        result = run_ontopo(["--help"])
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower() or "Usage:" in result.stdout
        assert "--date" in result.stdout
        assert "--time" in result.stdout
        assert "--restaurant" in result.stdout
        assert "--batch" in result.stdout


class TestOntopoCliValidation:
    """Test input validation."""

    def test_invalid_date_format(self, run_ontopo):
        """Invalid date format should error."""
        result = run_ontopo(["--date", "2026-01-31"])  # Wrong format (has dashes)
        assert result.returncode == 1
        assert "Invalid date format" in result.stdout or "Invalid date" in result.stderr

    def test_invalid_time_format(self, run_ontopo):
        """Invalid time format should error."""
        result = run_ontopo(["--date", "20260201", "--time", "19:00"])  # Has colon
        assert result.returncode == 1
        assert "Invalid time format" in result.stdout or "Invalid time" in result.stderr


@pytest.mark.live_api
class TestOntopoCliSingleRestaurant:
    """Test single restaurant search (hits real API)."""

    def test_search_by_slug(self, run_ontopo, tomorrow_date, sample_ontopo_slug):
        """Search by numeric slug should return results or graceful error."""
        result = run_ontopo([
            "--restaurant", sample_ontopo_slug,
            "--date", tomorrow_date,
            "--time", "1900",
            "--no-log",
        ])
        # Success OR graceful API response (not a crash)
        assert result.returncode == 0 or "Error" in result.stdout

    def test_raw_json_output(self, run_ontopo, tomorrow_date, sample_ontopo_slug, parse_json):
        """--raw should output valid JSON."""
        result = run_ontopo([
            "--restaurant", sample_ontopo_slug,
            "--date", tomorrow_date,
            "--time", "1900",
            "--raw",
            "--no-log",
        ])
        if result.returncode == 0:
            data = parse_json(result.stdout)
            assert isinstance(data, dict)
            # Response should have areas key (even if empty)
            assert "areas" in data or "error" in str(data).lower()

    def test_party_size_4(self, run_ontopo, tomorrow_date, sample_ontopo_slug):
        """Search with party size 4 should work."""
        result = run_ontopo([
            "--restaurant", sample_ontopo_slug,
            "--date", tomorrow_date,
            "--time", "1900",
            "--people", "4",
            "--no-log",
        ])
        # Should not crash
        assert result.returncode == 0 or "Error" in result.stdout


@pytest.mark.live_api
@pytest.mark.slow
class TestOntopoCliBatchMode:
    """Test batch mode (hits real API, slower)."""

    @pytest.mark.timeout(120)
    def test_batch_runs(self, run_ontopo, tomorrow_date):
        """Batch mode should run and output results."""
        result = run_ontopo([
            "--batch",
            "--date", tomorrow_date,
            "--time", "1900",
            "--workers", "10",
            "--no-log",
        ], timeout=120)
        # Batch should complete (may have no availability)
        assert result.returncode == 0
        # Should mention checking restaurants
        assert "Batch check:" in result.stdout or "restaurant" in result.stdout.lower()

    @pytest.mark.timeout(120)
    def test_batch_raw_json(self, run_ontopo, tomorrow_date, parse_json):
        """Batch mode with --raw should output JSON array."""
        result = run_ontopo([
            "--batch",
            "--date", tomorrow_date,
            "--time", "1900",
            "--workers", "10",
            "--raw",
            "--no-log",
        ], timeout=120)
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

    @pytest.mark.timeout(120)
    def test_batch_multiple_times(self, run_ontopo, tomorrow_date):
        """Batch mode with multiple times should work."""
        result = run_ontopo([
            "--batch",
            "--date", tomorrow_date,
            "--time", "1900",
            "--time", "2100",
            "--workers", "10",
            "--no-log",
        ], timeout=120)
        assert result.returncode == 0
