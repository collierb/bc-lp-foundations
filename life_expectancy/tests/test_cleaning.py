"""Tests for the cleaning module"""

import pandas as pd
from unittest.mock import patch, Mock

from life_expectancy.cleaning import clean_data, load_data, save_data


def test_clean_data(input_df, expected_df):
    """Run the `clean_data` function and compare the output to the expected output,
    using the sample fixtures created in the sample_fixtures.ipynb notebook
    and referenced in the conftest.py file"""
    actual_df = clean_data(input_df)
    pd.testing.assert_frame_equal(actual_df, expected_df)


@patch("life_expectancy.cleaning.pd.read_csv")
def test_load_data(read_csv_mock: Mock):
    """running and checking load_data on a mock dataframe"""
    read_csv_mock.return_value = pd.DataFrame({"life_exp": [78, 79, 77]})
    actual_df = load_data()
    read_csv_mock.assert_called_once()
    pd.testing.assert_frame_equal(actual_df, read_csv_mock.return_value)


def test_save_data():
    """running and checking save_data on a mock dataframe,
    save_data function in life_expectancy.py modified to return
    a dataframe for purpose of this test"""
    test_df = pd.DataFrame(
        {
            "unit": ["YR", "YR", "YR"],
            "sex": ["F", "F", "F"],
            "age": ["Y1", "Y1", "Y1"],
            "region": ["FR", "PT", "DE"],
            "year": [2020, 2020, 2020],
            "value": [78.2, 79.3, 77.1],
        }
    )
    with patch("pandas.DataFrame.to_csv") as to_csv_mock:
        to_csv_mock.return_value = print("mocking pandas to_csv method")
        # no required return value
        actual_df = save_data(test_df, "PT")
        expected_df = test_df[test_df["region"] == "PT"].reset_index(drop=True)
        pd.testing.assert_frame_equal(actual_df, expected_df)
        to_csv_mock.assert_called_once()
