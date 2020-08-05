from typing import Dict
from pathlib import Path

import pandas as pd
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal, assert_series_equal
import pytest

from fuzzymatch_records.parse_addresses import (
    _extract_dublin_postcodes,
    _remove_dublin_postcodes,
    _extract_address_numbers,
)

CWD = Path(__file__).parent
DATA = CWD / "data"


@pytest.fixture
def raw_addresses() -> Dict[str, pd.DataFrame]:

    return pd.read_csv(DATA / "RawAddresses.csv", squeeze=True, index_col=0)


def test_extract_dublin_postcodes(raw_addresses, ref) -> None:

    input = raw_addresses
    output = _extract_dublin_postcodes(input)

    expected_output = pd.read_csv(
        DATA / "DublinPostcodesExtracted.csv", squeeze=True, index_col=0
    )
    assert_series_equal(output, expected_output, check_names=False)


def test_remove_dublin_postcodes(raw_addresses) -> None:

    input = raw_addresses
    output = _remove_dublin_postcodes(input)

    expected_output = pd.read_csv(
        DATA / "DublinPostcodesRemoved.csv", squeeze=True, index_col=0
    )
    assert_series_equal(output, expected_output, check_names=False)


def test_extract_address_numbers(raw_addresses) -> None:

    input = raw_addresses
    output = _extract_address_numbers(input)

    expected_output = pd.read_csv(
        DATA / "AddressNumbersExtracted.csv", squeeze=True, index_col=0
    )
    assert_series_equal(output, expected_output, check_names=False)

