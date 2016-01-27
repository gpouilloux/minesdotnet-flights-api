from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.json_util import dumps
import os

app = Flask(__name__)

# HTTP GET /flights
# @param date [format=YYYY-mm-dd] : date of departure
# @param airport_departure : airport of departure
# @param airport_arrival : airport of arrival
# @return list of flights matching criteria
@app.route("/flights", methods=['GET'])
def flights():
    uri = os.environ['MONGOLAB_URI']
    if uri is None:
        client = MongoClient('localhost', 27017)
        db = client.test
    else:
        client = MongoClient(uri)
        db = client.get_default_database

    date = request.args.get('date')
    airport_departure = request.args.get('airport_departure')
    airport_arrival = request.args.get('airport_arrival')

    date_departure = datetime.strptime(date, '%Y-%m-%d')

    if date_departure is None or airport_departure is None or airport_arrival is None:
        abort(400)

    return dumps(db.flights.find({  "date_departure": {'$lt': (date_departure + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
                                                       '$gte': (date_departure - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S")},
                                    "airport_departure": airport_departure,
                                    "airport_arrival": airport_arrival}))

if __name__ == "__main__":
    server_port = os.environ['PORT']
    if(server_port is None):
        server_port = 5000
    app.run(debug='true',port=server_port)
