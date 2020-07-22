from typing import Dict
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from link_records.deduplicate import deduplicate_fuzzy_columns

CWD = Path(__file__).parent
DATA = CWD / "data"


@pytest.fixture
def duplicated_data() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(DATA / "duplicated_data.ods", sheet_name=None, engine="odf")


def test_deduplicate_fuzzy_columns(duplicated_data) -> None:

    input = duplicated_data["duplicates"]
    expected_output = duplicated_data["deduplicates"]

    output = deduplicate_fuzzy_columns(input, on_fuzzy=["Location"])
