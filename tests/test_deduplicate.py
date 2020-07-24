from pathlib import Path
from typing import Dict, Any

import icontract
import pandas as pd
import pytest
from fuzzymatch_records.deduplicate import deduplicate_dataframe_columns
from pandas.testing import assert_frame_equal

CWD = Path(__file__).parent
DATA = CWD / "data"


@pytest.fixture
def duplicates() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(DATA / "Duplicates.ods", sheet_name=None, engine="odf")


@pytest.mark.parametrize("input_sheet", ["duplicates", "not_duplicates"])
def test_deduplicate_dataframe_with_data(duplicates, input_sheet) -> None:

    input = duplicates[input_sheet]

    output = deduplicate_dataframe_columns(input, ["Location", "PB Name"], [0.8, 0.8])


@pytest.fixture
def breaking_inputs() -> Dict[str, Any]:

    df = pd.DataFrame([1, 2, 3])
    columns = ["blah"]
    min_similarities = [0.1]

    return {
        "not_a_dataframe": [1, columns, min_similarities],
    }


@pytest.mark.parametrize(
    "key", ["not_a_dataframe",],
)
def test_deduplicate_dataframe_raises_error(breaking_inputs, key) -> None:

    df, columns, min_similarities = breaking_inputs[key]

    with pytest.raises(icontract.ViolationError):
        deduplicate_dataframe_columns(df, columns, min_similarities)
