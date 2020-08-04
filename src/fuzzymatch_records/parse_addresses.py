from re import IGNORECASE, VERBOSE

import pandas as pd
from IPython.core.debugger import set_trace


def _extract_dublin_postcodes(series: pd.Series) -> pd.Series:

    return series.str.extract(pat=r"(dublin \d+\w?)", flags=IGNORECASE)[0]


def extract_dublin_postcodes(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Extracts numeric county names (Dublin 1, Dublin 2 etc) from the
    specified address column.  Won't extract Dublin County addresses

    Parameters
    ----------
    df : pd.DataFrame
    column : str
        Name of address column

    Returns
    -------
    pd.DataFrame
    """
    return df.assign(extracted_postcodes=df[column].pipe(_extract_dublin_postcodes))


def _remove_dublin_postcodes(series: pd.Series) -> pd.Series:

    return series.str.replace(pat=r"(dublin \d+\w?)", repl="", flags=IGNORECASE)


def remove_dublin_postcodes(df: pd.DataFrame, column: str) -> pd.DataFrame:

    return df.assign(**{column: df[column].pipe(_remove_dublin_postcodes).astype(str)})


def _extract_address_numbers(series: pd.Series) -> pd.Series:

    import ipdb

    ipdb.set_trace()

    pattern = """
    (
        \w*         # (optional) Starts with letters (ex: M4)
        \d+         # All numeric characters 
        [/-]?       # (optional) '-' or '/' (ex: 19/...)
        \d*         # (optional) second group of numbers (ex: 19/20)
        \w*         # (optional) Ends with letters (1st)
    )"""

    return series.str.extract(pat=pattern, flags=IGNORECASE | VERBOSE)[0]


def extract_address_numbers(df: pd.DataFrame, column: str) -> pd.DataFrame:

    return df.assign(address_numbers=df[column].pipe(_extract_address_numbers))
