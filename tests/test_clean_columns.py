from typing import Dict
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from link_records.clean_columns import clean_fuzzy_columns

CWD = Path(__file__).parent
DATA = CWD / "data"


@pytest.fixture
def mnr_three() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(DATA / "M&R [sample 3].ods", sheet_name=None, engine="odf")


@pytest.mark.parametrize(
    "input_key,expected_output_key", [("left", "left_clean"), ("right", "right_clean")]
)
def test_clean_fuzzy_columns(mnr_three, input_key, expected_output_key) -> None:

    input = mnr_three[input_key]
    expected_output = mnr_three[expected_output_key]

    output = clean_fuzzy_columns(input, fuzzy_cols=["Location", "PB Name"])

    assert_frame_equal(output, expected_output)
