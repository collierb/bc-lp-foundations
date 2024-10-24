"""Pytest configuration file"""

from pathlib import Path
import pandas as pd
import pytest

FIXTURE_DIR = Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def input_df():
    return pd.read_csv(FIXTURE_DIR / "eu_life_expectancy_sample_raw.tsv", sep="\t")


@pytest.fixture
def expected_df():
    return pd.read_csv(FIXTURE_DIR / "eu_life_expectancy_sample_expected.csv")
