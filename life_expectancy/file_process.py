"""file processing functions dependent on file type"""

import pandas as pd


def csv_clean(loaded_df: pd.DataFrame) -> pd.DataFrame:
    """clean csv data and reshape to long format"""
    loaded_df[["unit", "sex", "age", "region"]] = loaded_df[
        "unit,sex,age,geo\\time"
    ].str.split(",", expand=True)
    loaded_df.drop(columns="unit,sex,age,geo\\time", inplace=True)
    long_df = pd.melt(
        loaded_df,
        id_vars=["unit", "sex", "age", "region"],
        var_name="year",
        value_name="value",
    )
    long_df["year"] = long_df.year.str.strip().astype("int64")
    long_df["value"] = long_df.value.str.split(expand=True)[0]
    long_df["value"] = pd.to_numeric(long_df.value, errors="coerce")
    long_df.dropna(inplace=True)
    long_df.reset_index(inplace=True, drop=True)
    return long_df


def json_clean(loaded_df: pd.DataFrame) -> pd.DataFrame:
    """process json data"""
    loaded_df.drop(columns=["flag", "flag_detail"], inplace=True)
    loaded_df.rename(
        columns={"country": "region", "life_expectancy": "value"}, inplace=True
    )  # name change to mimic the csv file - minimal change to test modules
    return loaded_df
