from typing import Dict
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
from string_grouper import match_strings
from fuzzymatch_records.fuzzymatch import fuzzymatch_dataframes

CWD = Path(__file__).parent
DATA = CWD / "data"


# @pytest.fixture(params=["CompaniesFuzzyMatches", "AddressesFuzzyMatches"])
# def fuzzymatched_data(request) -> Dict[str, pd.DataFrame]:

#     return pd.read_excel(DATA / f"{request.param}.ods", sheet_name=None, engine="odf")


# @pytest.mark.parametrize(
#     "input_sheet, output_sheet",
#     [
#         ("fuzzymatches", "fuzzymatches_result"),
#         ("not_fuzzymatches", "not_fuzzymatches_result"),
#     ],
# )
# def test_match_most_similar_for_data(
#     fuzzymatched_data, input_sheet, output_sheet
# ) -> None:

#     input = fuzzymatched_data[input_sheet]
#     left, right = input["left"], input["right"]
#     # expected_output = fuzzymatched_data[output_sheet]

#     output = match_strings(left, right, min_similarity=0)
#     import ipdb

#     ipdb.set_trace()
#     assert_frame_equal(
#         output,
#         expected_output,
#         check_less_precise=True,
#         check_dtype=False,
#         check_like=True,
#     )


@pytest.fixture
def example_dataset() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(DATA / "ExampleDataset.ods", sheet_name=None, engine="odf")


# def test_fuzzymatch_dataframes(example_dataset) -> None:

#     left = example_dataset["left"]
#     right = example_dataset["right"]

#     pb_name_min_similarity = 0.8
#     location_min_similarity = 0.7
#     expected_output = example_dataset["matched_pb0_8_loc0_7"]

#     output = fuzzymatch_dataframes(
#         left,
#         right,
#         [("PB Name", pb_name_min_similarity), ("Location", location_min_similarity)],
#     )

#     assert_frame_equal(
#         output,
#         expected_output,
#         check_less_precise=True,
#         check_dtype=False,
#         check_like=True,
#     )
