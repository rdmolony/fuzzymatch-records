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


def deduplicate_dataframe(
    df: pd.DataFrame, fuzzy_column_properties: List[Tuple[str, float]],
) -> pd.DataFrame:

    on_fuzzy, min_similarities = zip(*fuzzy_column_properties)

    df = df.copy().pipe(clean_fuzzy_columns, on_fuzzy)

    for fuzzy_column, min_similarity in zip(on_fuzzy, min_similarities):

        df[fuzzy_column + "_deduplicated"] = group_similar_strings(
            df[fuzzy_column], min_similarity=min_similarity
        )

    return df


# def deduplicate_dataframe_via_string_grouper(
#     df: pd.DataFrame, fuzzy_columns: List[Tuple[str]],
# ):

#     columns, types = zip(*fuzzy_columns)
#     df = clean_fuzzy_columns(df, columns)

#     deduplicate_fuzzy_columns(df, columns, types)

