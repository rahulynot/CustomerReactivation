# CustomerReactivation

A small application demonstrating end-to-end machine learning project.

## Use case:
Create a solution for customer reactivation based on voucher offers. Based on previous vouchers sent to customers in different geographies, segment the customers based on their frequency of orders or their last order. Predict the most common voucher for that customer segment.

Based on the dataset, it's a fairly stratight-forward problem where the aim is to find the most common voucher amount. It can be done with a simple lookup table as well. In order to demonstrate end-to-end machine learning, a simple ML model is used to learn these patterns.

## Usage
$ cd CustomerReactivation

$ pip install -r requirements.txt #Possibly in a virtual env

### Tests
$ make test

### Build Docker Image
$ make build-image

### Run the Application Container
$ make run-app

### REST interface
The application can be accessed using a REST interface endpoint 'http://localhost:5000/predict'

$ curl --header \
"Content-Type: application/json" \
--request POST   --data '{"customer_id": 123,"country_code": "Peru", "last_order_ts": "2020-01-03 00:00:00","first_order_ts": "2017-05-03 00:00:00","total_orders": 15,"segment_name": "recency_segment"}'  \
http://localhost:5000/predict
