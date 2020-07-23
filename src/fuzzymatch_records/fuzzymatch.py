import re
from typing import List, Tuple
from pathlib import Path
from logging import Logger
import logging
import os
import sys

import pandas as pd
import numpy as np
from string_grouper import (
    match_most_similar,
    match_strings,
    StringGrouper,
    group_similar_strings,
)
import recordlinkage

from fuzzymatch_records.clean_columns import clean_fuzzy_column, clean_fuzzy_columns


def fuzzymatch_dataframes(
    left: pd.DataFrame,
    right: pd.DataFrame,
    fuzzy_column_properties: List[Tuple[str, float]],
) -> pd.DataFrame:

    left = left.copy()
    right = right.copy()

    on_fuzzy, min_similarities = zip(*fuzzy_column_properties)

    left = left.pipe(clean_fuzzy_columns, on_fuzzy)
    right = right.pipe(clean_fuzzy_columns, on_fuzzy)

    for fuzzy_column, min_similarity in zip(on_fuzzy, min_similarities):

        right[fuzzy_column + "_fuzzymatched"] = match_most_similar(
            left[fuzzy_column], right[fuzzy_column], min_similarity=min_similarity
        )

    return right


def calculate_fuzzymatches_for_min_similarity(
    left: pd.DataFrame, right: pd.DataFrame, column: str, min_similarity: float,
) -> pd.DataFrame:

    left_clean = left[column].drop_duplicates().pipe(clean_fuzzy_column)
    right_clean = right[column].drop_duplicates().pipe(clean_fuzzy_column)

    return match_strings(left_clean, right_clean, min_similarity=min_similarity)
