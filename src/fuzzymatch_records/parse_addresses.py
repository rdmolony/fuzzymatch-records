from re import IGNORECASE

import pandas as pd
from IPython.core.debugger import set_trace


def _parse_address_column(series: pd.Series) -> pd.DataFrame:

    return (
        series.rename("address")
        .to_frame()
        .pipe(extract_dublin_postcodes)
        .pipe(remove_dublin_postcodes)
        .pipe(extract_address_numbers)
    )


def parse_address_column(df: pd.DataFrame, column: str) -> pd.DataFrame:

    address = _parse_address_column(df[column])
    return pd.concat([df, address], axis="columns")


def _extract_dublin_postcodes(series: pd.Series) -> pd.Series:

    return series.str.extract(
        pat=r"((co\.? )?dublin ?(\d+)?(\(?county\)?)?)+", flags=IGNORECASE
    )[0]


def extract_dublin_postcodes(df: pd.DataFrame) -> pd.DataFrame:

    return df.assign(postcodes=_extract_dublin_postcodes(df.address))


def _remove_dublin_postcodes(series: pd.Series) -> pd.Series:

    return series.str.replace(
        pat=r"((co\.? )?dublin ?(\d+)?(\(?county\)?)?)+", repl="", flags=IGNORECASE
    )


def remove_dublin_postcodes(df: pd.DataFrame) -> pd.DataFrame:

    return df.assign(address=_remove_dublin_postcodes(df.address))


def _extract_address_numbers(series: pd.Series) -> pd.Series:

    return series.str.extract(
        pat=r"((block )?(unit )?(\w-?)?\d+\w{0,2}(-?/?\d+)?(.? floor)?)+",
        flags=IGNORECASE,
    )[0]


def extract_address_numbers(df: pd.DataFrame) -> pd.DataFrame:

    return df.assign(address_numbers=_extract_address_numbers(df.address))
