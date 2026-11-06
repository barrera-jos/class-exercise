import logging
import pandas as pd
import re
logger = logging.getLogger(__name__)


logging.basicConfig(filename='overview.log', level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def show_overview(df):
    """Display basic information about a DataFrame."""
    # TODO 1:
    # Log a DEBUG message containing the shape.
    
# 2. Log your debug message
    logging.debug(f"Here is the dataframe shape: {df.shape}")

    # Print the shape, first five rows, column names, and data types.
    print(df.shape,
          df.head(),
          list(df.columns),
          df.dtypes
          )

def remove_duplicates(df):
    """Remove exact duplicate rows."""
    # TODO 2:
    # Remove exact duplicate rows.
    before = len(df)
    df.drop_duplicates()
    # Log a DEBUG message containing the before and after row counts.
    logging.debug(f"removed {before-len(df)}")
    # Return the resulting DataFrame.
    return df


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    # TODO 3:
    # Drop rows containing one or more missing values.
    df.dropna()
    before = len(df)
    # Log a DEBUG message containing the before and after row counts.
    logging.debug(f"removed rows with missing values: {before-len(df)}")
    # Return the resulting DataFrame.

def clean_text(value):
    """Normalize one text value."""
    # TODO 1:
    # Strip surrounding whitespace.
    value = value.strip()
    # Convert text to lowercase.
    value = value.lower()
    # Collapse repeated whitespace.
    value = re.sub(r"\s+", " ", value)
    
    return value


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    # TODO 2:
    # If column does not exist:
    # Log an ERROR message and raise ValueError.
    if column not in df.columns:
        logger.error(f"Column '{column}' not found.")
        raise ValueError(f"Column '{column}' not found.")
    # Calculate Q1, Q3, and IQR.
    # Use threshold to calculate lower and upper bounds.
    # Keep rows inside the bounds.
    before = len(df)
    
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    

    lower = q1 - threshold * iqr
    upper = q3 + threshold * iqr
    
    df = df[(df[column]>=lower) & (df[column]<=upper)]
    
    # Log a DEBUG message containing the bounds and the number of rows removed.
    # Return the resulting DataFrame.
    
    logging.debug(f"Threshold: {threshold}, rows removed: {before - len(df)}")
    
    return df