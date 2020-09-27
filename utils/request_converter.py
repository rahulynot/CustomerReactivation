import pandas as pd
from datetime import datetime

VALID_COUNTRY_CODES = ["Australia", "China", "Latvia", "Peru"]
COUNTRY_CODE_FIELD = "country_code"
LAST_ORDER_TS_FIELD = "last_order_ts"


class RequestConverter:
    def __init__(self, request: dict):
        self.request = request
        self.country_code = None
        self.last_order_ts = None

    def is_valid(self) -> bool:
        if COUNTRY_CODE_FIELD not in self.request:
            raise KeyError(f"Missing/Incorrect field {COUNTRY_CODE_FIELD} in the request")

        if self.request[COUNTRY_CODE_FIELD] not in VALID_COUNTRY_CODES:
            raise ValueError(
                f"Invalid  {COUNTRY_CODE_FIELD} {self.request[COUNTRY_CODE_FIELD]} in the request"
            )
        else:
            self.country_code = self.request[COUNTRY_CODE_FIELD]

        if LAST_ORDER_TS_FIELD not in self.request:
            raise KeyError(f"Missing/Incorrect field {LAST_ORDER_TS_FIELD} in the request")

        # Parse 'last_order_ts' field
        else:
            try:
                self.last_order_ts = datetime.strptime(
                    self.request[LAST_ORDER_TS_FIELD], "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                raise ValueError(
                    f"Invalid {LAST_ORDER_TS_FIELD} {self.request[LAST_ORDER_TS_FIELD]} in the request"
                )

    def convert(self) -> pd.DataFrame:
        pass