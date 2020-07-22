from typing import Dict
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from link_records.fuzzymatch import (
    replace_fuzzy_columns_with_fuzzymatched_columns,
    fuzzymerge_dataframes,
)

CWD = Path(__file__).parent
DATA = CWD / "data"


@pytest.fixture
def mnr_three() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(DATA / "M&R [sample 3].ods", sheet_name=None, engine="odf")


def test_replace_fuzzy_columns_with_fuzzymatched_columns(mnr_three) -> None:

    left = mnr_three["left_clean"]
    right = mnr_three["right_clean"]
    expected_output = mnr_three["right_fuzzy_replaced"]

    output = replace_fuzzy_columns_with_fuzzymatched_columns(
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
