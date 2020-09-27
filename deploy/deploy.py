from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from ..utils.request_converter import RequestConverter

app = Flask(__name__)
api = Api(app)

MODEL_FREQUENT_SEGMENT = "../artifacts/freq_segment_model.pickle.dat"
MODEL_RECENCY_SEGMENT = "../artifacts/rec_segment_model.pickle.dat"


class PredictVoucherAmounts(Resource):
    def __init__(self):
        pass

    @staticmethod
    def post():
        request_data = request.get_json()
        req_conv = RequestConverter(request_data)

        try:
            features_df, segement = req_conv.convert()
        except Exception as e:
            return jsonify({"Error": str(e)})

        return jsonify({"Success": "Feature Generation done"})


api.add_resource(PredictVoucherAmounts, "/predict")

if __name__ == "__main__":
    app.run(debug=True)
