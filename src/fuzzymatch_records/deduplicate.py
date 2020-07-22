from typing import List, Tuple

import pandas as pd
import numpy as np
from string_grouper import (
    match_most_similar,
    match_strings,
    StringGrouper,
    group_similar_strings,
)


from fuzzymatch_records.clean_columns import clean_fuzzy_columns


def deduplicate_fuzzy_columns(
    df: pd.DataFrame, fuzzy_columns: List[str],
):

    for fuzzy_col in on_fuzzy:

        import ipdb

        ipdb.set_trace()

        df[fuzzy_col + "_before_deduplication"] = df[fuzzy_col]
        # df[fuzzy_col] = match_strings(df[fuzzy_col])
        df[fuzzy_col] = group_similar_strings(df[fuzzy_col])


def deduplicate_dataframe_via_string_grouper(
    df: pd.DataFrame, fuzzy_columns: List[Tuple[str]],
):

    columns, types = zip(*fuzzy_columns)
    df = clean_fuzzy_columns(df, columns)

    deduplicate_fuzzy_columns(df, columns, types)

