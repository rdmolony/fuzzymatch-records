from typing import List, Tuple

import icontract
import pandas as pd
import numpy as np
from string_grouper import (
    match_most_similar,
    match_strings,
    StringGrouper,
    group_similar_strings,
)


from fuzzymatch_records.clean_columns import clean_fuzzy_columns


@icontract.require(lambda df: isinstance(df, pd.DataFrame))
def deduplicate_dataframe_columns(
    df: pd.DataFrame, columns: List[str], min_similarities: List[float],
) -> pd.DataFrame:
    """Deduplicates columns for according to the min_similarity specified for 
    each column.

    Example
    -------
    deduplicate_dataframe_columns(df, ['company_name', 'address'], [0.9, 0.6])
    0.9 represents the minimum allowable (cossine) similarity between the
    'company_name' rows to define them as duplicates

    See https://github.com/Bergvca/string_grouper for more information on 
    fuzzy matching

    Parameters
    ----------
    df : pd.DataFrame
    columns : List[str]
    min_similarities : List[float]

    Returns
    -------
    pd.DataFrame
    """
    df = df.copy().pipe(clean_fuzzy_columns, columns)

    for column, min_similarity in zip(columns, min_similarities):

        df[column + "_deduplicated"] = group_similar_strings(
            df[column], min_similarity=min_similarity
        )

    return df
