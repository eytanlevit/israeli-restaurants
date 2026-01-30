"""CSV integrity tests for restaurants.csv."""

import csv
import re
from pathlib import Path

import pytest


class TestCsvExists:
    """Test CSV file exists and is readable."""

    def test_csv_exists(self, restaurants_csv_path):
        """restaurants.csv should exist."""
        assert restaurants_csv_path.exists(), f"CSV not found: {restaurants_csv_path}"

    def test_csv_has_required_columns(self, restaurants_csv_path):
        """CSV should have name, provider, id columns."""
        with open(restaurants_csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []
            assert "name" in fieldnames, "Missing 'name' column"
            assert "provider" in fieldnames, "Missing 'provider' column"
            assert "id" in fieldnames, "Missing 'id' column"


class TestCsvDataIntegrity:
    """Test data integrity rules."""

    @pytest.fixture
    def csv_rows(self, restaurants_csv_path) -> list[dict]:
        """Load all rows from CSV."""
        with open(restaurants_csv_path, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def test_all_entries_have_provider_and_id(self, csv_rows):
        """Every row should have provider and id."""
        for i, row in enumerate(csv_rows, start=2):  # Start at 2 (1 = header)
            name = row.get("name", f"row {i}")
            assert row.get("provider"), f"Row {i} ({name}): missing provider"
            assert row.get("id"), f"Row {i} ({name}): missing id"

    def test_valid_providers_only(self, csv_rows):
        """Providers should be 'ontopo' or 'tabit' only."""
        valid_providers = {"ontopo", "tabit"}
        for i, row in enumerate(csv_rows, start=2):
            provider = row.get("provider", "")
            name = row.get("name", f"row {i}")
            assert provider in valid_providers, (
                f"Row {i} ({name}): invalid provider '{provider}' "
                f"(expected: {valid_providers})"
            )

    def test_ontopo_ids_are_8_digits(self, csv_rows):
        """OnTopo IDs should be 8-digit numbers."""
        for i, row in enumerate(csv_rows, start=2):
            if row.get("provider") != "ontopo":
                continue
            id_val = row.get("id", "")
            name = row.get("name", f"row {i}")
            assert re.match(r"^\d{8}$", id_val), (
                f"Row {i} ({name}): OnTopo ID '{id_val}' is not 8 digits"
            )

    def test_tabit_ids_are_24_char_hex(self, csv_rows):
        """Tabit IDs should be 24-character hex strings."""
        for i, row in enumerate(csv_rows, start=2):
            if row.get("provider") != "tabit":
                continue
            id_val = row.get("id", "")
            name = row.get("name", f"row {i}")
            assert re.match(r"^[0-9a-f]{24}$", id_val), (
                f"Row {i} ({name}): Tabit ID '{id_val}' is not 24-char hex"
            )

    def test_no_duplicate_ids(self, csv_rows):
        """IDs should be unique within each provider."""
        ontopo_ids = []
        tabit_ids = []
        for row in csv_rows:
            provider = row.get("provider", "")
            id_val = row.get("id", "")
            name = row.get("name", "")
            if provider == "ontopo":
                assert id_val not in ontopo_ids, f"Duplicate OnTopo ID: {id_val} ({name})"
                ontopo_ids.append(id_val)
            elif provider == "tabit":
                assert id_val not in tabit_ids, f"Duplicate Tabit ID: {id_val} ({name})"
                tabit_ids.append(id_val)

    def test_no_duplicate_names(self, csv_rows):
        """Restaurant names should be unique."""
        names = []
        for row in csv_rows:
            name = row.get("name", "")
            assert name not in names, f"Duplicate restaurant name: {name}"
            names.append(name)


class TestCsvProviderCounts:
    """Test minimum provider counts."""

    @pytest.fixture
    def csv_rows(self, restaurants_csv_path) -> list[dict]:
        """Load all rows from CSV."""
        with open(restaurants_csv_path, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def test_minimum_ontopo_count(self, csv_rows):
        """Should have at least 35 OnTopo restaurants."""
        ontopo_count = sum(1 for r in csv_rows if r.get("provider") == "ontopo")
        assert ontopo_count >= 35, f"Only {ontopo_count} OnTopo restaurants (need >= 35)"

    def test_minimum_tabit_count(self, csv_rows):
        """Should have at least 5 Tabit restaurants."""
        tabit_count = sum(1 for r in csv_rows if r.get("provider") == "tabit")
        assert tabit_count >= 5, f"Only {tabit_count} Tabit restaurants (need >= 5)"
