import logging

logger = logging.getLogger(__name__)

def require_columns(df, required_columns):
    """Check that all required columns exist."""
    # Check if any of the configured columns (list) are missing from df.
    # If any are missing, log an ERROR and raise ValueError.
    # Log an INFO.
    # Return the DataFrame.
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        logger.error(f"Missing required columns: {missing}")
        raise ValueError(f"Missing required columns: {missing}")

    logger.info(f"All required columns present: {required_columns}")
    return df