from ...deploy.deploy import app
from flask import json


def test_deploy_returns_404_for_unknown_endpoint():
    response = app.test_client().post("/unknown")
    assert response.status_code == 404

    response = app.test_client().post("/")
    assert response.status_code == 404


def test_deploy_returns_error_on_invalid_request():
    response = app.test_client().post(
        "/predict", data=json.dumps({"a": 1, "b": 2}), content_type="application/json",
    )

    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data["Error"] == "'Missing/Incorrect field country_code in the request'"


def test_deploy_returns_prediction():
    valid_request = {
        "customer_id": 123,  # customer id
        "country_code": "Peru",  # customer’s country
        "last_order_ts": "2018-05-03 00:00:00",  # ts of the last order placed by a customer
        "first_order_ts": "2017-05-03 00:00:00",  # ts of the first order placed by a customer
        "total_orders": 15,  # total orders placed by a customer
        "segment_name": "recency_segment",  # which segment a customer belongs to
    }

    response = app.test_client().post(
        "/predict", data=json.dumps(valid_request), content_type="application/json",
    )

    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data["Success"] == "Feature Generation done"
