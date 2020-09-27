from datetime import datetime

import pytest

from ...utils.common import Segment
from ...utils.request_converter import (
    COUNTRY_CODE_FIELD,
    LAST_ORDER_TS_FIELD,
    SEGMENT_NAME_FIELD,
    TOTAL_ORDER_FIELD,
    RequestConverter,
)


def test_is_valid_fails_for_invalid_country_code_key():
    requests = [
        {"customer_id": 123,},  # Missing country_code
        {"customer_id": 123, "code_country": "Peru",},  # Incorrect value
    ]

    for request in requests:

        req_conv = RequestConverter(request)

        with pytest.raises(KeyError) as excinfo:
            req_conv.is_valid()
        assert "Missing/Incorrect field country_code in the request" in str(excinfo.value)


def test_is_valid_fails_for_invalid_country_code_value():
    request = {"customer_id": 123, "country_code": "Japan"}  # Incorrect value

    req_conv = RequestConverter(request)

    with pytest.raises(ValueError) as excinfo:
        req_conv.is_valid()
    assert f"Invalid  {COUNTRY_CODE_FIELD} Japan" in str(excinfo.value)


def test_is_valid_fails_for_invalid_last_order_ts_key():

    requests = [
        # Missing last_order_ts
        {"customer_id": 123, "country_code": "Peru",},
        # Incorrect key value of last_order_ts
        {"customer_id": 123, "country_code": "Peru", "last_order": "2018-05-03 00:00:00",},
    ]

    for request in requests:

        req_conv = RequestConverter(request)

        with pytest.raises(KeyError) as excinfo:
            req_conv.is_valid()
        assert f"Missing/Incorrect field {LAST_ORDER_TS_FIELD} in the request" in str(excinfo.value)


def test_is_valid_fails_for_invalid_last_order_ts_value():

    requests = [
        # Missing last_order_ts value
        {"customer_id": 123, "country_code": "Peru", "last_order_ts": "",},
        # Incorrect value of last_order_ts
        {"customer_id": 123, "country_code": "Peru", "last_order_ts": "Invalid-value",},
    ]

    for request in requests:

        req_conv = RequestConverter(request)

        with pytest.raises(ValueError) as excinfo:
            req_conv.is_valid()
        assert f"Invalid last_order_ts {request['last_order_ts']} in the request" in str(
            excinfo.value
        )


def test_is_valid_fails_for_invalid_total_orders_key():

    requests = [
        # Missing total_orders value
        {"customer_id": 123, "country_code": "Peru", "last_order_ts": "2018-05-03 00:00:00",},
        # Incorrect key name for total_orders
        {
            "customer_id": 123,
            "country_code": "Peru",
            "last_order_ts": "2018-05-03 00:00:00",
            "order_totals": 15,
        },
    ]

    for request in requests:

        req_conv = RequestConverter(request)

        with pytest.raises(KeyError) as excinfo:
            req_conv.is_valid()
        assert f"Missing/Incorrect field {TOTAL_ORDER_FIELD} in the request" in str(excinfo.value)


def test_is_valid_fails_for_invalid_total_orders_value():

    request = {
        "customer_id": 123,
        "country_code": "Peru",
        "last_order_ts": "2018-05-03 00:00:00",
        "total_orders": "invalid-value",
    }

    req_conv = RequestConverter(request)

    with pytest.raises(ValueError) as excinfo:
        req_conv.is_valid()
    assert f"Invalid {TOTAL_ORDER_FIELD} invalid-value in the request" in str(excinfo.value)


def test_is_valid_fails_for_invalid_segment_name_key():

    requests = [
        # Missing segment_nam value
        {
            "customer_id": 123,
            "country_code": "Peru",
            "last_order_ts": "2018-05-03 00:00:00",
            "total_orders": 15,
        },
        # Incorrect key name for total_orders
        {
            "customer_id": 123,
            "country_code": "Peru",
            "last_order_ts": "2018-05-03 00:00:00",
            "total_orders": 15,
            "some_segment": "",
        },
    ]

    for request in requests:

        req_conv = RequestConverter(request)

        with pytest.raises(KeyError) as excinfo:
            req_conv.is_valid()
        assert f"Missing/Incorrect field {SEGMENT_NAME_FIELD} in the request" in str(excinfo.value)


def test_is_valid_fails_for_invalid_segment_name_value():

    request = {
        "customer_id": 123,
        "country_code": "Peru",
        "last_order_ts": "2018-05-03 00:00:00",
        "total_orders": 15,
        "segment_name": "invalid_segment",
    }

    req_conv = RequestConverter(request)

    with pytest.raises(ValueError) as excinfo:
        req_conv.is_valid()
    assert f"Invalid {SEGMENT_NAME_FIELD} invalid_segment" in str(excinfo.value)


def test_is_valid_succeeds_for_valid_request():

    valid_request = {
        "customer_id": 123,  # customer id
        "country_code": "Peru",  # customer’s country
        "last_order_ts": "2018-05-03 00:00:00",  # ts of the last order placed by a customer
        "first_order_ts": "2017-05-03 00:00:00",  # ts of the first order placed by a customer
        "total_orders": 15,  # total orders placed by a customer
        "segment_name": "recency_segment",  # which segment a customer belongs to
    }

    req_conv = RequestConverter(valid_request)

    assert req_conv.is_valid() == True
    assert req_conv.country_code == "Peru"
    assert (
        req_conv.last_order_ts
        == datetime.strptime(valid_request[LAST_ORDER_TS_FIELD], "%Y-%m-%d %H:%M:%S").date()
    )
    assert req_conv.total_orders == 15
    assert req_conv.segment_name == Segment.RECENCY


def test_convert_request():
    pass
