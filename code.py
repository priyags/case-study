from flask import Flask, request
from flask_restful import Api
import json
from expiringdict import ExpiringDict
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--ttl", type=int, help="Enter a ttl", #adjustable ttl
                    nargs='?', default=30, const=0)
args = parser.parse_args()


app = Flask(__name__)
api = Api(app)

cache_dict = ExpiringDict(max_len=1000, max_age_seconds=args.ttl)


# Save data
@app.route('/save_data', methods=['POST'])
def save_data():
    mdata = request.get_json(force=True)
    cache_dict[mdata.get('id')] = mdata
    return "Successfully saved the message - {} with the id - {}".format(mdata['message'], mdata['id'])


# Get data
@app.route('/get_data/<int:id>', methods=['GET'])
def get_data(id):
    try:
        if cache_dict[id]:
            return_value = cache_dict.get(id)
            print("Value from the cache dictionary - ", return_value)
            response = app.response_class(
                response=json.dumps(return_value),
                status=200,
                mimetype='application/json'
            )
            return response
    except KeyError:
        return "Resource Not Found!"


if __name__ == '__main__':
    app.run(debug=False)
