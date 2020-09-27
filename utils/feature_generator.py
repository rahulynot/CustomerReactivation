import pandas as pd
import numpy as np

from .common import Segment


def convert_to_bins(bins: list, labels: list, df_to_cut: pd.DataFrame) -> pd.DataFrame:
    return pd.cut(df_to_cut, bins=bins, labels=labels, include_lowest=True)


def generate_frequent_segment_features(df: pd.DataFrame) -> pd.DataFrame:
    bins = [0.0, 4.0, 13.0, 37.0, np.inf]
    labels = ["0-4", "5-13", "13-37", "38-higher"]

    df["total_orders_ranges"] = convert_to_bins(bins, labels, df["total_orders"])

    one_hot_freq_segment = pd.get_dummies(df["total_orders_ranges"], prefix="freq")
    df = df.drop("total_orders_ranges", axis=1)
    df = df.join(one_hot_freq_segment)

    return df


def generate_recency_segment_features(df: pd.DataFrame) -> pd.DataFrame:
    bins = [0.0, 30, 60, 90, 120, 180, np.inf]
    labels = ["0-30", "30-60", "60-90", "90-120", "120-180", "180+"]

    df["recency_segment_ranges"] = convert_to_bins(bins, labels, df["days_since_last_order"])

    one_hot_rec_segment = pd.get_dummies(df["recency_segment_ranges"], prefix="rec_segment")
    df = df.drop("recency_segment_ranges", axis=1)
    df = df.join(one_hot_rec_segment)

    return df


def generate_features(df: pd.DataFrame, segment_name: Segment) -> pd.DataFrame:
    if segment_name == Segment.FREQUENT:
        return generate_frequent_segment_features(df)
    else:
        return generate_recency_segment_features(df)
