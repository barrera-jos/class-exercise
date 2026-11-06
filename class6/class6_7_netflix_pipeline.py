import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    clean_text,
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers,
    show_overview,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    # TODO 4
    data_path = Path(args.input)
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        logger.error("file not found")
        sys.exit(1)
        
    logger.info(f"Dataset loaded: {args.input}")

    # TODO 5
    #show_overview(df)
    #logger.info("Overview Displayed")

    # TODO 6
    before = len(df)
    df = remove_duplicates(df)
    logger.info(f"Removed {before - len(df)} duplicate row(s)")
 
    before = len(df)
    df = drop_missing_rows(df)
    logger.info(f"Dropped {before - len(df)} rows with missing values")
    
    
    # TODO 3:
    # Inside a try block, remove runtime_minutes outliers
    # using remove_iqr_outliers() with a threshold of 1.5.
    # Catch ValueError and exit with sys.exit(1).# Log an INFO message.
    
    try:
        df = remove_iqr_outliers(df, 'runtime_minutes', 1.5)
    except ValueError:
        sys.exit(1)
    logger.info('removing outliers using iqr')

    # TODO 4:
    # Apply clean_text() to title, type, and country.
    # Log an INFO message.
    for col in ['title', 'type', 'country']:
        
        df['title'].apply(clean_text)
        logger.info(f'Column {col} cleaned')
    # TODO 5:
    # Create a report (dictionary) containing rows_before, rows_after, rows_removed, and columns.
    # Log an INFO message reporting: rows_before, rows_after, rows_removed, and columns.
    report = {'rows_before': len(before), 'rows_after': len(df), 'rows_removed': len(before) - len(df)}
    
    logger.info(f'Report: {report}')

if __name__ == "__main__":
    main()