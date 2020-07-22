from typing import List

import pandas as pd
from ftfy import fix_text
from unidecode import unidecode


def clean_fuzzy_columns(df: pd.DataFrame, fuzzy_cols: List[str]) -> pd.DataFrame:

    for fuzzy_col in fuzzy_cols:

        df[fuzzy_col] = (
            df[fuzzy_col]
            .apply(fix_text)
            .apply(unidecode)
            .str.replace("&", "and")
            .str.replace(r"[,-./]|\sBD", "")
            .str.title()
            .str.pad(width=1, side="both", fillchar=" ")
        )

    return df
