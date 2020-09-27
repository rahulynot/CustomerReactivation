from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from utils.request_converter import RequestConverter
from utils.feature_generator import generate_features

from utils.common import Segment

import pickle

app = Flask(__name__)
api = Api(app)

MODEL_FREQUENT_SEGMENT = "artifacts/freq_segment_model.pickle.dat"
MODEL_RECENCY_SEGMENT = "artifacts/rec_segment_model.pickle.dat"


class PredictVoucherAmounts(Resource):
    def __init__(self):
        self.frequent_model = pickle.load(open(MODEL_FREQUENT_SEGMENT, "rb"))
        self.recency_model = pickle.load(open(MODEL_RECENCY_SEGMENT, "rb"))

    def post(self):
        request_data = request.get_json()
        req_conv = RequestConverter(request_data)

        try:
            features_df, segement = req_conv.convert()
        except Exception as e:
            return jsonify({"Error": str(e)})

        features = generate_features(features_df, segement)
        if segement == Segment.FREQUENT:
            voucher_amount = self.frequent_model.predict(features)
        elif segement == Segment.RECENCY:
            voucher_amount = self.recency_model.predict(features)

        return jsonify({"voucher_amount": voucher_amount[0]})


api.add_resource(PredictVoucherAmounts, "/predict")

if __name__ == "__main__":
    app.run(debug=True)
