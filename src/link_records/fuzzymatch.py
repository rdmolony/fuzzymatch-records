import re
from typing import List, Tuple
from pathlib import Path

from prefect import task


import pandas as pd
import numpy as np
from string_grouper import (
    match_most_similar,
    match_strings,
    StringGrouper,
    group_similar_strings,
)

from link_records.clean_columns import clean_fuzzy_columns


def replace_fuzzy_columns_with_fuzzymatched_columns(
    left: pd.DataFrame, right: pd.DataFrame, fuzzy_cols: List[str]
) -> pd.DataFrame:

    for fuzzy_col in fuzzy_cols:

        right[fuzzy_col + "_original"] = right[fuzzy_col]
        right[fuzzy_col] = match_most_similar(
            left[fuzzy_col].fillna(""), right[fuzzy_col].fillna(""), min_similarity=0.1
        )

    return right


def fuzzymerge_dataframes(
    left: pd.DataFrame, right: pd.DataFrame, on_fuzzy: List[str], on_smooth: List[str],
) -> pd.DataFrame:

    left = clean_fuzzy_columns(left, on_fuzzy)
    right = clean_fuzzy_columns(right, on_fuzzy)
    right = replace_fuzzy_columns_with_fuzzymatched_columns(left, right, on_fuzzy)

    merge_columns = on_fuzzy + on_smooth

    return pd.merge(left, right, on=merge_columns)
