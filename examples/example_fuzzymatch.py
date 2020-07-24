from pathlib import Path

from string_grouper import StringGrouper, match_most_similar
import pandas as pd

from fuzzymatch_records.clean_columns import clean_fuzzy_column
from fuzzymatch_records.deduplicate import deduplicate_dataframe_columns
from fuzzymatch_records.fuzzymatch import (
    calculate_fuzzymatches_for_min_similarity,
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


if __name__ == "__main__":

    # Parse address column for easy differentiation of building numbers etc.
    # ... tf-idf struggles with 15 blah road and 17 blah road
    # Also deduplicate company names first by matching strings over thresold ...
    left = (
        example_sheets["left"]
        .pipe(parse_address_column, "Location")
        .pipe(deduplicate_dataframe_columns, ["PB Name"], [0.8])
    )
    right = (
        example_sheets["right"]
        .pipe(parse_address_column, "Location")
        .pipe(deduplicate_dataframe_columns, ["PB Name"], [0.8])
    )

    # Use to inspect results for given min_similarity ...
    test_pb_matches = calculate_fuzzymatches_for_min_similarity(
        left, right, on="PB Name", min_similarity=0.8,
    )
    print(f"Number of fuzzy matches on PB Name = {len(test_pb_matches)}/{len(left)}")

    test_loc_matches = calculate_fuzzymatches_for_min_similarity(
        left, right, on="Location", min_similarity=0.7,
    )
    print(f"Number of fuzzy matches on Location = {len(test_loc_matches)}/{len(left)}")

    right_fuzzymatched = fuzzymatch_dataframes(
        left, right, on_fuzzy=["PB Name", "Location"], min_similarities=[0.8, 0.5]
    )

    merged_raw = pd.merge(
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

    raw_results = CWD / "RawExampleMergeResults.csv"
    merged_raw.to_csv(raw_results)
    print(f"Raw merge results saved to {raw_results}")

    select_results = CWD / "SelectExampleMergeResults.csv"
    merged_raw[
        [
            "PB Name_deduplicated_left",
            "address_numbers_left",
            "Location_parsed_left",
            "Attributable Total Final Consumption (kWh)_left",
            "address_numbers_right",
            "Location_parsed_right",
            "PB Name_deduplicated_right",
            "Attributable Total Final Consumption (kWh)_right",
        ]
    ].to_csv(select_results)
    print(f"Select merge results saved to {raw_results}")

    ## Uncomment to fiddle with results for better grouping performance
    # via StringGrouper as explained in https://github.com/Bergvca/string_grouper

    # pb_name_grouper = StringGrouper(
    #     left["PB Name"], right["PB Name"], min_similarity=0.8
    # ).fit()

    # location_grouper = StringGrouper(
    #     left["Location"],
    #     right["Location"],
    #     min_similarity=0.4,
    # ).fit()

