import numpy as np
import pandas as pd
import pytest
from pandas._testing import assert_frame_equal

from ...utils import feature_generator
from ...utils.common import Segment

expected_freq_frame_data = {
    "freq_0-4": [0],
    "freq_5-13": [0],
    "freq_13-37": [1],
    "freq_38-higher": [0],
    "country_code_Australia": [0],
    "country_code_China": [0],
    "country_code_Latvia": [0],
    "country_code_Peru": [1],
}

expected_rec_frame_data = {
    "rec_segment_0-30": [0],
    "rec_segment_30-60": [1],
    "rec_segment_60-90": [0],
    "rec_segment_90-120": [0],
    "rec_segment_120-180": [0],
    "country_code_Australia": [0],
    "country_code_China": [0],
    "country_code_Latvia": [0],
    "country_code_Peru": [1],
}


def test_generate_features():
    freq_data = {
        "total_orders": [15],
        "days_since_last_order": [45],
        "last_order_ts": ["2018-01-01"],
        "timestamp": ["2018-01-01"],
        "country_code": "Peru",
    }
    df = pd.DataFrame.from_dict(freq_data)
    generated_frame = feature_generator.generate_features(df, Segment.FREQUENT)

    expected_frame = pd.DataFrame.from_dict(expected_freq_frame_data)
    assert_frame_equal(expected_frame, generated_frame, check_dtype=False)

    rec_data = {
        "days_since_last_order": [45],
        "total_orders": [15],
        "last_order_ts": ["2018-01-01"],
        "timestamp": ["2018-01-01"],
        "country_code": "Peru",
    }
    df = pd.DataFrame.from_dict(rec_data)
    generated_frame = feature_generator.generate_features(df, Segment.RECENCY)

    expected_frame = pd.DataFrame.from_dict(expected_rec_frame_data)
    assert_frame_equal(expected_frame, generated_frame, check_dtype=False)
