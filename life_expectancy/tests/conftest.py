"""Pytest configuration file"""

from pathlib import Path
import pandas as pd
import pytest

FIXTURE_DIR = Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def input_df():
    # return pd.read_csv(FIXTURE_DIR / "eu_life_expectancy_sample_raw.tsv", sep="\t")
    return pd.read_json(FIXTURE_DIR / "eurostat_sample_raw.json", orient="index")


@pytest.fixture
def expected_df():
    # return pd.read_csv(FIXTURE_DIR / "eu_life_expectancy_sample_expected.csv")
    return pd.read_json(FIXTURE_DIR / "eurostat_sample_expected.json", orient="index")
