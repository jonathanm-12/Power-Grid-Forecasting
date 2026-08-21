"""
Contains generator, decorators, and set operations.
Module name: utils.py
"""

import time
from functools import wraps


def runtime_logger(func):
    """
    Decorator logging runtime of any function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        out = func(*args, **kwargs)
        print(f"{func.__name__} executed in {time.time() - start:.4f} sec")
        return out

    return wrapper


def hourly_load_generator(df):
    """
    Streams load entries row-by-row.
    """
    for _, row in df.iterrows():
        yield row


def unique_outage_days(outage_df):
    """
    Example set operation.
    """
    return set(outage_df['start_time'].dt.date)