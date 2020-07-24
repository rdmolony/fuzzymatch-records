from typing import List

import pandas as pd
import icontract
from ftfy import fix_text
from unidecode import unidecode


@icontract.require(lambda series: isinstance(series, pd.Series))
@icontract.require(lambda series: not series.empty)
def clean_fuzzy_column(series: pd.Series) -> pd.Series:

    return (
        series.astype(str)
        .apply(fix_text)
        .apply(unidecode)
        .str.replace("&", "and")
        .str.replace(r"[,-./]|\sBD", " ")
        .str.replace("  ", " ")
        .str.title()
        .str.pad(width=1, side="both", fillchar=" ")
    )


def clean_fuzzy_columns(df: pd.DataFrame, fuzzy_cols: List[str]) -> pd.DataFrame:

    for fuzzy_column in fuzzy_cols:
        df.loc[:, fuzzy_column] = clean_fuzzy_column(df[fuzzy_column])

    return df
