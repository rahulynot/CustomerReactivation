import pytest

from ...utils.request_converter import RequestConverter

sample_request = {
    "customer_id": 123,  # customer id
    "country_code": "Peru",  # customer’s country
    "last_order_ts": "2018-05-03 00:00:00",  # ts of the last order placed by a customer
    "first_order_ts": "2017-05-03 00:00:00",  # ts of the first order placed by a customer
    "total_orders": 15,  # total orders placed by a customer
    "segment_name": "recency_segment",  # which segment a customer belongs to
}


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
    assert "Invalid  country_code Japan in the request" in str(excinfo.value)


def test_is_valid_fails_for_invalid_last_order_ts():

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
        assert "Missing/Incorrect field last_order_ts in the request" in str(excinfo.value)


def test_convert_request():
    pass
