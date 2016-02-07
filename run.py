from flask import Flask, request, abort
from flask.ext.cors import CORS, cross_origin
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.json_util import dumps
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Check is a property has been provided or not
def notProvided(property):
    return property is None or property == ''

# Error handle for HTTP code 400
@app.errorhandler(400)
def badRequest(error):
    return "{}\nThe server was not able to process your request because it is malformed.".format(error)

# HTTP GET /flights
# @param date [format=YYYY-mm-dd] : date of departure
# @param airport_departure : airport of departure
# @param airport_arrival : airport of arrival
# @param flexible : number of days before and after the flight [optional]
# @return list of flights matching criteria
@app.route("/flights", methods=['GET'])
@cross_origin()
def flights():
    uri = os.environ.get('MONGOLAB_URI', 'mongodb://localhost:27017/test')
    client = MongoClient(uri)

    db = client.get_default_database()
    date = request.args.get('date')
    airport_departure = request.args.get('airport_departure')
    airport_arrival = request.args.get('airport_arrival')
    flexible = request.args.get('flexible', '1')

    # returns all flights if no parameter is provided
    if date is None and airport_departure is None and airport_arrival is None:
        return dumps(db.flights.find())

    # bad request
    if notProvided(date) or notProvided(airport_departure) or notProvided(airport_arrival):
        abort(400)

    date_departure = datetime.strptime(date, '%Y-%m-%d')
    return dumps(db.flights.find({  "date_departure": {'$lt': (date_departure + timedelta(days=int(flexible))).strftime("%Y-%m-%dT%H:%M:%S"),
                                                       '$gte': (date_departure - timedelta(days=int(flexible))).strftime("%Y-%m-%dT%H:%M:%S")},
                                    "airport_departure": airport_departure,
                                    "airport_arrival": airport_arrival}))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug='true', host='0.0.0.0', port=int(port))
