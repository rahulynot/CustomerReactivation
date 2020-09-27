from datetime import datetime

import numpy as np
import pandas as pd

from .common import VALID_COUNTRY_CODES, Segment

COUNTRY_CODE_FIELD = "country_code"
LAST_ORDER_TS_FIELD = "last_order_ts"
TOTAL_ORDER_FIELD = "total_orders"
SEGMENT_NAME_FIELD = "segment_name"
CURRENT_TS_FIELD = "timestamp"


def convert_segment_name(segment_name: str) -> Segment:

    if segment_name == "recency_segment":
        return Segment.RECENCY
    elif segment_name == "frequent_segment":
        return Segment.FREQUENT

    raise ValueError(f"Invalid {SEGMENT_NAME_FIELD} {segment_name}")


class RequestConverter:
    def __init__(self, request: dict):
        self.request = request
        self.country_code = None
        self.last_order_ts = None
        self.total_orders = None
        self.segment_name = None
        self.current_ts = datetime.now().date()

    def is_valid(self) -> bool:
        # Parse 'country_code' field
        if COUNTRY_CODE_FIELD not in self.request:
            raise KeyError(f"Missing/Incorrect field {COUNTRY_CODE_FIELD} in the request")

        if self.request[COUNTRY_CODE_FIELD] not in VALID_COUNTRY_CODES:
            raise ValueError(
                f"Invalid  {COUNTRY_CODE_FIELD} {self.request[COUNTRY_CODE_FIELD]} in the request"
            )
        else:
            self.country_code = self.request[COUNTRY_CODE_FIELD]

        # Parse 'last_order_ts' field
        if LAST_ORDER_TS_FIELD not in self.request:
            raise KeyError(f"Missing/Incorrect field {LAST_ORDER_TS_FIELD} in the request")
        else:
            try:
                self.last_order_ts = datetime.strptime(
                    self.request[LAST_ORDER_TS_FIELD], "%Y-%m-%d %H:%M:%S"
                ).date()

                if self.last_order_ts > self.current_ts:
                    raise ValueError()

            except ValueError:
                raise ValueError(
                    f"Invalid {LAST_ORDER_TS_FIELD} {self.request[LAST_ORDER_TS_FIELD]} in the request"
                )

        # Parse 'total_orders' field
        if TOTAL_ORDER_FIELD not in self.request:
            raise KeyError(f"Missing/Incorrect field {TOTAL_ORDER_FIELD} in the request")
        else:
            if type(self.request[TOTAL_ORDER_FIELD]) != int:
                raise ValueError(
                    f"Invalid {TOTAL_ORDER_FIELD} {self.request[TOTAL_ORDER_FIELD]} in the request"
                )

            self.total_orders = int(self.request[TOTAL_ORDER_FIELD])

        # Parse 'segment_name' field
        if SEGMENT_NAME_FIELD not in self.request:
            raise KeyError(f"Missing/Incorrect field {SEGMENT_NAME_FIELD} in the request")
        else:
            try:
                self.segment_name = convert_segment_name(self.request[SEGMENT_NAME_FIELD])
            except ValueError as e:
                raise ValueError(e)

        return True

    def convert(self) -> (pd.DataFrame, Segment):

        try:
            self.is_valid()
        except Exception as e:
            raise ValueError(e)

        df_dict = {
            CURRENT_TS_FIELD: [self.current_ts],
            TOTAL_ORDER_FIELD: [self.total_orders],
            COUNTRY_CODE_FIELD: [self.country_code],
            LAST_ORDER_TS_FIELD: [self.last_order_ts],
        }

        df = pd.DataFrame(data=df_dict, dtype=np.int)

        if self.segment_name == Segment.RECENCY:
            df["days_since_last_order"] = (df["timestamp"] - df["last_order_ts"]).dt.days

        return df, self.segment_name
