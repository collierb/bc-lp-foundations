"""preprocess data"""

from pathlib import Path
import argparse
import pandas as pd
from life_expectancy.region import Region

PARENT_PATH = Path(__file__).parent


def load_data() -> pd.DataFrame:
    """load raw life expectancy data file stored in data folder"""
    df = pd.read_csv(PARENT_PATH / "data" / "eu_life_expectancy_raw.tsv", sep="\t")
    return df


def clean_data(loaded_df: pd.DataFrame) -> pd.DataFrame:
    """clean data and reshape to long format."""
    loaded_df[["unit", "sex", "age", "region"]] = loaded_df[
        "unit,sex,age,geo\\time"
    ].str.split(",", expand=True)
    # tab seperation from the load_data above left one column needing to be split on the comma
    loaded_df.drop(columns="unit,sex,age,geo\\time", inplace=True)
    long_df = pd.melt(
        loaded_df,
        id_vars=["unit", "sex", "age", "region"],
        var_name="year",
        value_name="value",
    )
    long_df["year"] = long_df.year.str.strip().astype("int64")
    long_df["value"] = long_df.value.str.split(expand=True)[0]
    # whitespace seperated out various non-numeric references in variable value
    long_df["value"] = pd.to_numeric(long_df.value, errors="coerce")
    # coerce ensures all "" entries converted to NaN
    long_df.dropna(inplace=True)
    long_df.reset_index(inplace=True, drop=True)
    return long_df


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
