from io import StringIO
from typing import Dict
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from fuzzymatch_records.fuzzymatch_records import (
    _deduplicate_fuzzy_columns,
    _clean_fuzzy_columns,
    _replace_fuzzy_columns_with_fuzzymatched_columns,
    fuzzymerge_dataframes,
)

CWD = Path(__file__).parent
DATA = CWD / "data"


@pytest.fixture
def mnr_three() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(DATA / "M&R [sample ].ods", sheet_name=None, engine="odf")


@pytest.fixture
def mnr_hundred() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(DATA / "M&R [sample 100].ods", sheet_name=None, engine="odf")


@pytest.fixture
def duplicated_data() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(DATA / "duplicated_data.ods", sheet_name=None, engine="odf")


def test_deduplicate_fuzzy_columns(duplicated_data) -> None:

    input = duplicated_data["duplicates"]
    expected_output = duplicated_data["deduplicates"]

    output = _deduplicate_fuzzy_columns(input, on_fuzzy=["Location"])


@pytest.mark.parametrize(
    "input_key,expected_output_key", [("left", "left_clean"), ("right", "right_clean")]
)
def test_clean_fuzzy_columns(mnr_three, input_key, expected_output_key) -> None:

    input = mnr_three[input_key]
    expected_output = mnr_three[expected_output_key]

    output = _clean_fuzzy_columns(input, fuzzy_cols=["Location", "PB Name"])

    assert_frame_equal(output, expected_output)


def test_replace_fuzzy_columns_with_fuzzymatched_columns(mnr_three) -> None:

    left = mnr_three["left_clean"]
    right = mnr_three["right_clean"]
    expected_output = mnr_three["right_fuzzy_replaced"]

    output = _replace_fuzzy_columns_with_fuzzymatched_columns(
        left, right, fuzzy_cols=["PB Name", "Location"]
    )

    assert_frame_equal(output, expected_output)


def test_fuzzymerge_dataframes(mnr_three) -> None:

    left = mnr_three["left_clean"]
    right = mnr_three["right_clean"]
    expected_output = mnr_three["merged"]

    output = fuzzymerge_dataframes(
        left,
        right,
        on_fuzzy=["Location", "PB Name"],
        on_smooth=["Consumption Category", "County", "Year"],
    )

    assert_frame_equal(output, expected_output)
