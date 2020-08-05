from pathlib import Path
from typing import Any, Dict

import icontract
import pandas as pd
import pytest
from fuzzymatch_records.fuzzymatch import (
    fuzzymatch_dataframes,
    calculate_fuzzymatches_for_min_similarity,
)
from pandas.testing import assert_frame_equal
from string_grouper import match_strings

CWD = Path(__file__).parent
DATA = CWD / "data"


# @pytest.fixture(params=["CompaniesFuzzyMatches", "AddressesFuzzyMatches"])
# def fuzzymatched_data(request) -> Dict[str, pd.DataFrame]:

#     return pd.read_excel(DATA / f"{request.param}.ods", sheet_name=None, engine="odf")


# @pytest.mark.parametrize("min_similarity", [0, 0.5, 1])
# @pytest.mark.parametrize(
#     "input_sheet, output_sheet",
#     [
#         ("fuzzymatches", "fuzzymatches_result"),
#         ("not_fuzzymatches", "not_fuzzymatches_result"),
#     ],
# )
# def test_calculate_fuzzymatches_for_min_similarity_succeeds(
#     fuzzymatched_data, input_sheet, output_sheet, min_similarity
# ) -> None:

#     input = fuzzymatched_data[input_sheet]
#     left, right = input["left"], input["right"]

#     calculate_fuzzymatches_for_min_similarity(
#         left, right, left_on="left", right_on="right", min_similarity=0
#     )


# @pytest.fixture(
#     scope="module",
#     params=[
#         "FuzzyMatchOnSameFuzzyColumns.ods",
#         "FuzzyMatchOnDifferentFuzzyColumns.ods",
#     ],
# )
# def data_to_fuzzymatch(request) -> Dict[str, pd.DataFrame]:

#     return pd.read_excel(DATA / request.param, sheet_name=None, engine="odf")


# @pytest.mark.parametrize("min_similarity", [(0, 0), (0.5, 0.5), (1, 1)])
# def test_fuzzymatch_dataframes_on_data(data_to_fuzzymatch, ref, min_similarity) -> None:

#     left = data_to_fuzzymatch["left"]
#     right = data_to_fuzzymatch["right"]

#     fuzzymatch_dataframes(
#         left, right, on_fuzzy=["PB Name", "Location"], min_similarities=min_similarity,
#     )


@pytest.fixture
def breaking_inputs() -> Dict[str, Any]:

    left = pd.DataFrame([1, 2, 3])
    right = pd.DataFrame([1, 2, 3])
    on_fuzzy = ["blah"]
    min_similarity = [0.1]
    on_fuzzy_left = ["blah"]
    on_fuzzy_right = ["blah"]

    return {
        "empty_on_fuzzy": [left, right, None, min_similarity, None, None],
        "only_on_fuzzy_left": [left, right, None, min_similarity, on_fuzzy_left, None],
        "empty_min_similarity": [left, right, on_fuzzy, None, None, None],
        "string_min_similarity": [left, right, on_fuzzy, "imastring", None, None],
        "not_a_dataframe": [1, 2, on_fuzzy, min_similarity, None, None],
    }


@pytest.mark.parametrize(
    "key",
    [
        "empty_on_fuzzy",
        "only_on_fuzzy_left",
        "string_min_similarity",
        "empty_min_similarity",
        "not_a_dataframe",
    ],
)
def test_fuzzymatch_dataframes_raises_error(breaking_inputs, key) -> None:

    (
        left,
        right,
        on_fuzzy,
        on_fuzzy_left,
        on_fuzzy_right,
        min_similarities,
    ) = breaking_inputs[key]

    with pytest.raises(icontract.ViolationError):
        fuzzymatch_dataframes(
            left,
            right,
            on_fuzzy=on_fuzzy,
            on_fuzzy_left=on_fuzzy_left,
            on_fuzzy_right=on_fuzzy_right,
            min_similarity=min_similarities,
        )

