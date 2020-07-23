from typing import Dict
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal
from numpy.testing import assert_equal, assert_almost_equal
import pytest

from fuzzymatch_records.clean_columns import clean_fuzzy_column, clean_fuzzy_columns

CWD = Path(__file__).parent
DATA = CWD / "data"


@pytest.fixture
def dirty_fuzzy_data() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(
        DATA / "DirtyFuzzyData.ods", sheet_name=None, engine="odf", squeeze=True
    )


def test_clean_fuzzy_column(dirty_fuzzy_data) -> None:

    input = dirty_fuzzy_data["dirty_fuzzy_column"]
    expected_output = dirty_fuzzy_data["clean_fuzzy_column"]

    output = clean_fuzzy_column(input)

    assert_equal(output.array, expected_output.array)

