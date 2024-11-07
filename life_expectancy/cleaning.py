"""preprocess data"""

from pathlib import Path
import argparse
import pandas as pd
from life_expectancy.region import Region
from life_expectancy.file_process import json_clean

PARENT_PATH = Path(__file__).parent


def load_data() -> pd.DataFrame:
    """load raw life expectancy data file stored in data folder"""
    # df = pd.read_csv(PARENT_PATH / "data" / "eu_life_expectancy_raw.tsv", sep="\t")
    df = pd.read_json(PARENT_PATH / "data" / "eurostat_life_expect.json")
    return df


def clean_data(loaded_df: pd.DataFrame) -> pd.DataFrame:
    """clean data through file specific function, import needed"""
    # df = csv_clean(loaded_df)
    df = json_clean(loaded_df)
    return df


def save_data(cleaned_df: pd.DataFrame, country: Region) -> pd.DataFrame:
    """save the cleaned data to data folder"""
    country_df = cleaned_df[cleaned_df["region"] == country.value].reset_index(
        drop=True
    )
    country_df.to_csv(
        PARENT_PATH / "data" / f"{country.value}_life_expectancy.csv", index=False
    )
    # print(f"clean and filtered file for {country.value} saved to data folder")
    return country_df  # for testing purposes only


def preprocess_data(country: Region) -> None:
    """call load, clean and save functions.
    Optional country selection defauts to PT
    """
    loaded_df = load_data()
    cleaned_df = clean_data(loaded_df)
    save_data(cleaned_df, country)


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="country filter for life expectancy data"
    )
    parser.add_argument(
        "--country",
        type=Region,
        choices=list(Region),
        default="PT",
        help="select country in ISO2 format eg FR",
    )
    args = parser.parse_args()
    preprocess_data(args.country)
