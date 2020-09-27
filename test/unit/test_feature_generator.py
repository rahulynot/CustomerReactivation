import numpy as np
import pandas as pd
import pytest
from pandas._testing import assert_frame_equal

from ...utils import feature_generator
from ...utils.common import Segment

expected_freq_frame_data = {
    "total_orders": 15,
    "freq_0-4": [0],
    "freq_5-13": [0],
    "freq_13-37": [1],
    "freq_38-higher": [0],
}

expected_rec_frame_data = {
    "days_since_last_order": 45,
    "rec_segment_0-30": [0],
    "rec_segment_30-60": [1],
    "rec_segment_60-90": [0],
    "rec_segment_90-120": [0],
    "rec_segment_120-180": [0],
    "rec_segment_180+": [0],
}


def test_generate_frequent_segment_features():
    data = {"total_orders": [15]}
    df = pd.DataFrame.from_dict(data)
    generated_frame = feature_generator.generate_frequent_segment_features(df)

    expected_frame = pd.DataFrame.from_dict(expected_freq_frame_data)

    assert_frame_equal(expected_frame, generated_frame, check_dtype=False)


def test_generate_recency_segment_features():
    data = {"days_since_last_order": [45]}
    df = pd.DataFrame.from_dict(data)
    generated_frame = feature_generator.generate_recency_segment_features(df)

    expected_frame = pd.DataFrame.from_dict(expected_rec_frame_data)

    assert_frame_equal(expected_frame, generated_frame, check_dtype=False)


def test_generate_features():
    freq_data = {"total_orders": [15]}
    df = pd.DataFrame.from_dict(freq_data)
    generated_frame = feature_generator.generate_features(df, Segment.FREQUENT)

    expected_frame = pd.DataFrame.from_dict(expected_freq_frame_data)
    assert_frame_equal(expected_frame, generated_frame, check_dtype=False)

    rec_data = {"days_since_last_order": [45]}
    df = pd.DataFrame.from_dict(rec_data)
    generated_frame = feature_generator.generate_features(df, Segment.RECENCY)

    expected_frame = pd.DataFrame.from_dict(expected_rec_frame_data)
    assert_frame_equal(expected_frame, generated_frame, check_dtype=False)
