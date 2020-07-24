from typing import Dict
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from fuzzymatch_records.deduplicate import deduplicate_dataframe

CWD = Path(__file__).parent
DATA = CWD / "data"


@pytest.fixture
def duplicates() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(DATA / "Duplicates.ods", sheet_name=None, engine="odf")


@pytest.mark.parametrize(
    "input_sheet,output_sheet",
    [
        ("duplicates", "not_duplicates"),
        ("duplicates_deduplicated", "not_duplicates_deduplicated"),
    ],
)
def test_deduplicate_fuzzy_columns(duplicates, input_sheet, output_sheet) -> None:

    input = duplicates[input_sheet]
    expected_output = duplicates[output_sheet]

    output = deduplicate_dataframe(input, [("Location", 0.8), ("PB Name", 0.8)])
