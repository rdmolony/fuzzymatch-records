from pathlib import Path

from string_grouper import StringGrouper, match_most_similar
import pandas as pd

from fuzzymatch_records.clean_columns import clean_fuzzy_column
from fuzzymatch_records.fuzzymatch import (
    calculate_fuzzymatches_for_min_similarity_to_file,
    fuzzymatch_dataframes,
)
from fuzzymatch_records.parse_addresses import (
    extract_dublin_postcodes,
    remove_dublin_postcodes,
    extract_address_numbers,
)

CWD = Path(__file__).parent

example_sheets = pd.read_excel(
    CWD / "ExampleDataset.ods", sheet_name=None, engine="odf"
)


def _parse_address_column(series: pd.Series, column: str) -> pd.DataFrame:

    parsed_column = f"{column}_parsed"
    return (
        series.rename(parsed_column)
        .to_frame()
        .pipe(extract_dublin_postcodes, parsed_column)
        .pipe(remove_dublin_postcodes, parsed_column)
        .pipe(extract_address_numbers, parsed_column)
    )


def parse_address_column(df: pd.DataFrame, column: str) -> pd.DataFrame:

    df = df.copy()
    address_columns = _parse_address_column(df[column], column)
    return pd.concat([df, address_columns], axis="columns")


if __file__ == "__main__":

    # Parse address column for easy differentiation of building numbers etc.
    # ... tf-idf struggles with 15 blah road and 17 blah road
    left = example_sheets["left"].pipe(parse_address_column, "Location")
    right = example_sheets["right"].pipe(parse_address_column, "Location")

    pb_name_min_sim = 0.8
    location_min_sim = 0.7

    calculate_fuzzymatches_for_min_similarity_to_file(
        left, right, column="PB Name", min_similarity=pb_name_min_sim, dirpath=CWD
    )
    calculate_fuzzymatches_for_min_similarity_to_file(
        left, right, column="Location", min_similarity=location_min_sim, dirpath=CWD
    )

    right_fuzzymatched = fuzzymatch_dataframes(
        left, right, [("PB Name", pb_name_min_sim), ("Location", location_min_sim)],
    )

    merged = pd.merge(
        left,
        right_fuzzymatched,
        left_on=["PB Name", "Location", "Consumption Category"],
        right_on=[
            "PB Name_fuzzymatched",
            "Location_fuzzymatched",
            "Consumption Category",
        ],
        suffixes=("_left", "_right"),
    )

    ## Uncomment To fiddle with results as in https://github.com/Bergvca/string_grouper

    # pb_name_grouper = StringGrouper(
    #     left["PB Name"], right["PB Name"], min_similarity=0.8
    # ).fit()
    # location_grouper = StringGrouper(
    #     left["Location"],
    #     right["Location"],
    #     min_similarity=0.4,
    # ).fit()

