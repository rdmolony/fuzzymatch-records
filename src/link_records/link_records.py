import re
from typing import List, Tuple
from pathlib import Path

from ftfy import fix_text
import pandas as pd
import numpy as np
from string_grouper import (
    match_most_similar,
    match_strings,
    StringGrouper,
    group_similar_strings,
    StringGrouperConfig,
)
from unidecode import unidecode


def extract_address_number(vo: pd.Series) -> pd.Series:

    return series.str.extract(pat=r"(\d+/?\w*)")


def deduplicate_dataframe_via_string_grouper(
    df: pd.DataFrame, on_fuzzy: List[str], min_similarity: float = 0.8,
):

    df = _clean_fuzzy_columns(df, on_fuzzy)

    _deduplicate_fuzzy_columns(df, on_fuzzy, min_similarity)


def _deduplicate_fuzzy_columns(
    df: pd.DataFrame, on_fuzzy: List[str], min_similarity: float,
):

    for fuzzy_col in on_fuzzy:

        df[fuzzy_col + "_before_deduplication"] = df[fuzzy_col]
        df[fuzzy_col] = group_similar_strings(
            df[fuzzy_col], min_similarity=min_similarity
        )


def fuzzymatch_dataframes(
    left: pd.DataFrame,
    right: pd.DataFrame,
    on_fuzzy: List[str],
    on_smooth: List[str],
    min_similarity: float = 0.8,
) -> pd.DataFrame:

    left = _clean_fuzzy_columns(left, on_fuzzy)
    right = _clean_fuzzy_columns(right, on_fuzzy)

    return _replace_fuzzy_columns_with_fuzzymatched_columns(
        left, right, on_fuzzy, min_similarity
    )


def _clean_fuzzy_columns(df: pd.DataFrame, fuzzy_cols: List[str]) -> pd.DataFrame:

    for fuzzy_col in fuzzy_cols:

        df[fuzzy_col] = (
            df[fuzzy_col]
            .astype(str)
            .fillna("")
            .apply(fix_text)
            .apply(unidecode)
            .str.replace("&", "and")
            .str.replace(r"[,-./]|\sBD", "")
            .str.title()
            .str.pad(width=1, side="both", fillchar=" ")
        )

    return df


def _replace_fuzzy_columns_with_fuzzymatched_columns(
    left: pd.DataFrame,
    right: pd.DataFrame,
    fuzzy_cols: List[str],
    min_similarity: float,
) -> pd.DataFrame:

    for fuzzy_col in fuzzy_cols:

        right[fuzzy_col + "_before_fuzzymatching"] = right[fuzzy_col]
        right[fuzzy_col] = match_most_similar(
            left[fuzzy_col].fillna(""),
            right[fuzzy_col].fillna(""),
            min_similarity=min_similarity,
        )

    return right

