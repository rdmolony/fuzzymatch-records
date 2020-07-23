from re import IGNORECASE

import pandas as pd
from IPython.core.debugger import set_trace


def _extract_dublin_postcodes(series: pd.Series) -> pd.Series:

    return series.str.extract(
        pat=r"((co\.? )?dublin ?(\d+)?(\(?county\)?)?)+", flags=IGNORECASE
    )[0]


def extract_dublin_postcodes(df: pd.DataFrame, column: str) -> pd.DataFrame:

    return df.assign(postcodes=df[column].pipe(_extract_dublin_postcodes))


def _remove_dublin_postcodes(series: pd.Series) -> pd.Series:

    return series.str.replace(
        pat=r"((co\.? )?dublin ?(\d+)?(\(?county\)?)?)+", repl="", flags=IGNORECASE
    )


def remove_dublin_postcodes(df: pd.DataFrame, column: str) -> pd.DataFrame:

    return df.assign(**{column: df[column].pipe(_remove_dublin_postcodes).astype(str)})


def _extract_address_numbers(series: pd.Series) -> pd.Series:

    return series.str.extract(
        pat=r"((block )?(unit )?(\w-?)?\d+\w{0,2}(-?/?\d+)?(.? floor)?)+",
        flags=IGNORECASE,
    )[0]


def extract_address_numbers(df: pd.DataFrame, column: str) -> pd.DataFrame:

    return df.assign(address_numbers=df[column].pipe(_extract_address_numbers))
