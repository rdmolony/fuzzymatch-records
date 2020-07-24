from pathlib import Path
from typing import Dict, Any

import icontract
import pandas as pd
import pytest
from fuzzymatch_records.clean_columns import clean_fuzzy_column, clean_fuzzy_columns
from numpy.testing import assert_almost_equal, assert_equal
from pandas.testing import assert_frame_equal

CWD = Path(__file__).parent
DATA = CWD / "data"


@pytest.fixture
def dirty_fuzzy_data() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(
        DATA / "DirtyFuzzyData.ods", sheet_name=None, engine="odf", squeeze=True
    )


def test_clean_fuzzy_column_with_data(dirty_fuzzy_data) -> None:

    input = dirty_fuzzy_data["dirty_fuzzy_column"]
    expected_output = dirty_fuzzy_data["clean_fuzzy_column"]

    output = clean_fuzzy_column(input)

    assert_equal(output.array, expected_output.array)


@pytest.fixture
def breaking_inputs() -> Dict[str, Any]:

    return {
        "dataframe": pd.DataFrame([1, 2, 3]),
        "empty_series": pd.Series(),
    }


@pytest.mark.parametrize("key", ["dataframe", "empty_series"])
def test_clean_fuzzy_column_raises_error(breaking_inputs, key) -> None:

    input = breaking_inputs[key]

    with pytest.raises(icontract.ViolationError):
        clean_fuzzy_column(input)
