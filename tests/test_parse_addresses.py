from typing import Dict
from pathlib import Path

import pandas as pd
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal
import pytest

from fuzzymatch_records.parse_addresses import (
    _extract_dublin_postcodes,
    _remove_dublin_postcodes,
    _extract_address_numbers,
)

CWD = Path(__file__).parent
DATA = CWD / "data"


@pytest.fixture
def addresses() -> Dict[str, pd.DataFrame]:

    return pd.read_excel(
        DATA / "Addresses.ods", sheet_name=None, engine="odf", squeeze=True,
    )


def test_extract_dublin_postcodes(addresses) -> None:

    input = addresses["raw_addresses"]
    expected_output = addresses["extracted_postcodes"]

    output = _extract_dublin_postcodes(input).dropna()
    # assert_equal(output.array, expected_output.array)


def test_remove_dublin_postcodes(addresses) -> None:

    input = addresses["raw_addresses"]
    expected_output = addresses["addresses_without_postcodes"]

    output = _remove_dublin_postcodes(input)
    # assert_equal(output.array, expected_output.array)


def test_remove_dublin_postcodes(addresses) -> None:

    input = addresses["raw_addresses"]
    expected_output = addresses["addresses_without_postcodes"]

    output = _remove_dublin_postcodes(input)
    # assert_equal(output.array, expected_output.array)


def test_extract_address_numbers(addresses) -> None:

    input = addresses["addresses_without_postcodes"]
    expected_output = addresses["address_numbers"]

    output = _extract_address_numbers(input).dropna()
    # assert_equal(output.array, expected_output.array)

