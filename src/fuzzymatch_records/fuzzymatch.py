import logging
import os
import re
import sys
from logging import Logger
from pathlib import Path
from typing import List, Tuple, Union, Sequence

import icontract
import numpy as np
import pandas as pd
import recordlinkage
from fuzzymatch_records.clean_columns import clean_fuzzy_column, clean_fuzzy_columns
from string_grouper import (
    StringGrouper,
    group_similar_strings,
    match_most_similar,
    match_strings,
)


@icontract.require(
    lambda on_fuzzy, on_fuzzy_left, on_fuzzy_right: (on_fuzzy is not None)
    or ((on_fuzzy_left is not None) & (on_fuzzy_right is not None))
)
@icontract.require(lambda min_similarities: min_similarities is not None)
@icontract.require(
    lambda left, right: isinstance(left, pd.DataFrame) & isinstance(right, pd.DataFrame)
)
def fuzzymatch_dataframes(
    left: pd.DataFrame,
    right: pd.DataFrame,
    on_fuzzy: List[str] = None,
    on_fuzzy_left: List[str] = None,
    on_fuzzy_right: List[str] = None,
    min_similarities: List[float] = None,
) -> pd.DataFrame:
    """Fuzzymatches columns from 'left' to 'right' DataFrames
    according to the min_similarity specified for each column and replaces 
    the original columns in 'right' with the fuzzymatch result.

    Example
    -------
    fuzzymatch_dataframes(left, right, ['company_name', 'address'], [0.9, 0.6])
    0.9 represents the minimum allowable (cossine) similarity between the
    'company_name' columns in the 'left' and 'right' DataFrames to define
    the match_most_similar a success

    See https://github.com/Bergvca/string_grouper for more information on 
    fuzzy matching

    Parameters
    ----------
    left : pd.DataFrame
    right : pd.DataFrame
    on_fuzzy : List[str]
    on_fuzzy_left : List[str]
    on_fuzzy_right : List[str]
    min_similarities: List[float]

    Returns
    -------
    pd.DataFrame
    """
    if on_fuzzy:

        left = left.copy().pipe(clean_fuzzy_columns, on_fuzzy)
        right = right.copy().pipe(clean_fuzzy_columns, on_fuzzy)

        for fuzzy_column, min_similarity in zip(on_fuzzy, min_similarities):

            right[fuzzy_column] = match_most_similar(
                left[fuzzy_column], right[fuzzy_column], min_similarity=min_similarity
            )

    else:

        left = left.copy().pipe(clean_fuzzy_columns, on_fuzzy_left)
        right = right.copy().pipe(clean_fuzzy_columns, on_fuzzy_right)

        for (fuzzy_column_left, fuzzy_column_right, min_similarity) in zip(
            on_fuzzy_left, on_fuzzy_right, min_similarities,
        ):

            right[fuzzy_column_right] = match_most_similar(
                left[fuzzy_column_left],
                right[fuzzy_column_right],
                min_similarity=min_similarity,
            )

    return right


@icontract.require(
    lambda on, left_on, right_on: (on is not None)
    or ((left_on is not None) & (right_on is not None))
)
@icontract.require(lambda min_similarity: min_similarity is not None)
@icontract.require(
    lambda min_similarity: isinstance(min_similarity, float) or min_similarity == 0
)
@icontract.require(
    lambda left, right: (isinstance(left, pd.Series) & isinstance(right, pd.Series))
    or (isinstance(left, pd.DataFrame) & isinstance(right, pd.DataFrame))
)
def calculate_fuzzymatches_for_min_similarity(
    left: Union[pd.DataFrame, pd.Series],
    right: Union[pd.DataFrame, pd.Series],
    on: str = None,
    left_on: str = None,
    right_on: str = None,
    min_similarity: float = None,
) -> pd.DataFrame:

    if isinstance(left, pd.Series) and isinstance(right, pd.Series):
        left_clean = left.drop_duplicates().pipe(clean_fuzzy_column)
        right_clean = right.drop_duplicates().pipe(clean_fuzzy_column)

    elif on is not None:
        left_clean = left[on].drop_duplicates().pipe(clean_fuzzy_column)
        right_clean = right[on].drop_duplicates().pipe(clean_fuzzy_column)

    elif (left_on is not None) and (right_on is not None):
        left_clean = left[left_on].drop_duplicates().pipe(clean_fuzzy_column)
        right_clean = right[right_on].drop_duplicates().pipe(clean_fuzzy_column)

    else:
        raise ValueError("Unexpected condition...")

    match = match_strings(left_clean, right_clean, min_similarity=min_similarity)

    return match

