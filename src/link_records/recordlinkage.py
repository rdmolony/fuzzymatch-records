import re
from typing import List, Tuple
from pathlib import Path

from prefect import task

from ftfy import fix_text
import pandas as pd
import numpy as np
from string_grouper import (
    match_most_similar,
    match_strings,
    StringGrouper,
    group_similar_strings,
)
from unidecode import unidecode


def deduplicate_dataframe_via_string_grouper(
    df: pd.DataFrame, fuzzy_columns: List[Tuple[str]],
):

    columns, types = zip(*fuzzy_columns)
    df = _clean_fuzzy_columns(df, columns)

    _parse_addresses()
    _deduplicate_fuzzy_columns(df, columns, types)


def _deduplicate_fuzzy_columns(
    df: pd.DataFrame, fuzzy_columns: List[str],
):

    for fuzzy_col in on_fuzzy:

        import ipdb

        ipdb.set_trace()

        df[fuzzy_col + "_before_deduplication"] = df[fuzzy_col]
        # df[fuzzy_col] = match_strings(df[fuzzy_col])
        df[fuzzy_col] = group_similar_strings(df[fuzzy_col])


def fuzzymerge_dataframes(
    left: pd.DataFrame, right: pd.DataFrame, on_fuzzy: List[str], on_smooth: List[str],
) -> pd.DataFrame:

    left = _clean_fuzzy_columns(left, on_fuzzy)
    right = _clean_fuzzy_columns(right, on_fuzzy)
    right = _replace_fuzzy_columns_with_fuzzymatched_columns(left, right, on_fuzzy)

    merge_columns = on_fuzzy + on_smooth

    return pd.merge(left, right, on=merge_columns)


def _clean_fuzzy_columns(df: pd.DataFrame, fuzzy_cols: List[str]) -> pd.DataFrame:

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


def _replace_fuzzy_columns_with_fuzzymatched_columns(
    left: pd.DataFrame, right: pd.DataFrame, fuzzy_cols: List[str]
) -> pd.DataFrame:

    for fuzzy_col in fuzzy_cols:

        right[fuzzy_col + "_original"] = right[fuzzy_col]
        right[fuzzy_col] = match_most_similar(
            left[fuzzy_col].fillna(""), right[fuzzy_col].fillna(""), min_similarity=0.1
        )

    return right

