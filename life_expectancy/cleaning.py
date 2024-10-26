"""preprocess data"""

from pathlib import Path
import argparse
from enum import Enum
import pandas as pd

PARENT_PATH = Path(__file__).parent


class Region(Enum):
    """List of countries and regions in EU dataset and applicable codes.
    Note that these codes do not strictly conform to ISO2 standards,
    with notable examples Greece and United Kingdom."""

    AUSTRIA = "AT"
    BELGIUM = "BE"
    BULGARIA = "BG"
    SWITZERLAND = "CH"
    CYPRUS = "CY"
    CZECHIA = "CZ"
    DENMARK = "DK"
    ESTONIA = "EE"
    GREECE = "EL"
    SPAIN = "ES"
    EU27_2020 = "EU27_2020"
    FINLAND = "FI"
    FRANCE = "FR"
    CROATIA = "HR"
    HUNGARY = "HU"
    ICELAND = "IS"
    ITALY = "IT"
    LIECHTENSTEIN = "LI"
    LITHUANIA = "LT"
    LUXEMBOURG = "LU"
    LATVIA = "LV"
    MALTA = "MT"
    NETHERLANDS = "NL"
    NORWAY = "NO"
    POLAND = "PL"
    PORTUGAL = "PT"
    ROMANIA = "RO"
    SWEDEN = "SE"
    SLOVENIA = "SI"
    SLOVAKIA = "SK"
    GERMANY = "DE"
    DE_TOT = "DE_TOT"
    ALBANIA = "AL"
    EA18 = "EA18"
    EA19 = "EA19"
    EFTA = "EFTA"
    IRELAND = "IE"
    MONTENEGRO = "ME"
    NORTH_MACEDONIA = "MK"
    SERBIA = "RS"
    ARMENIA = "AM"
    AZERBAIJAN = "AZ"
    GEORGIA = "GE"
    TURKEY = "TR"
    UKRAINE = "UA"
    BELARUS = "BY"
    EEA30_2007 = "EEA30_2007"
    EEA31 = "EEA31"
    EU27_2007 = "EU27_2007"
    EU28 = "EU28"
    UNITED_KINGDOM = "UK"
    KOSOVO = "XK"
    METROPOLITAN_FRANCE = "FX"
    MOLDOVA = "MD"
    SAN_MARINO = "SM"
    RUSSIAN_FEDERATION = "RU"

    @classmethod
    def region_list(cls):
        """generate a list of actual countries for the EU dataset"""
        return [
            r.name
            for r in cls
            if r.value
            not in [
                "EU27_2020",
                "DE_TOT",
                "EA18",
                "EA19",
                "EFTA",
                "EEA30_2007",
                "EEA31",
                "EU27_2007",
                "EU28",
            ]
        ]

    def __str__(self):
        return self.value


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
