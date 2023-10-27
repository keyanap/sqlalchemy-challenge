# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
# List routes
    return(
        f"Available Routes for Hawaii Weather:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date><br/>"
        f"/api/v1.0/<start_date>/<end_date><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
# Create our session (link) from Python to the DB
    session = Session(engine)

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    precipititaion_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').\
        group_by(Measurement.date).order_by(Measurement.date).all()
    session.close()

# Return the JSON representation of your dictionary.
    precipititaion_results = []

    for date, prcp in precipititaion_query:
        precipititaion_dict = {}
        precipititaion_dict['precipitation'] = prcp
        precipititaion_dict['date'] = date
        precipititaion_results.append(precipititaion_dict)

    return jsonify(precipititaion_results)


@app.route("/api/v1.0/stations")
def station():
# Create our session (link) from Python to the DB
    session = Session(engine)
    station_query = session.query(Station.station, Station.id).all()
    
    session.close()
# Return a JSON list of stations from the dataset.
    stations_results = []
    for station, id in station_query:
        stations_dict = {}
        stations_dict['station'] = station
        stations_dict['id'] = id
        stations_results.append(stations_dict)

    return jsonify (stations_results)


@app.route("/api/v1.0/tobs")
def tobs():
# Create our session (link) from Python to the DB
    session = Session(engine)
# Query the dates and temperature observations of the most-active station for the previous year of data.
    most_active_query = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()
    session.close()

# Return a JSON list of temperature observations for the previous year.
    tobs_results = []
    for date, tobs, prcp in most_active_query:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_dict['prcp'] = prcp
        tobs_results.append(tobs_dict)

    return jsonify(tobs_results)


@app.route("/api/v1.0/<start_date>")
def start_date(start_date, end_date='2017-08-23'):
# Create our session (link) from Python to the DB
    session = Session(engine)
    start_date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    start_date_results = []
    for tmin, tavg, tmax in start_date_query:
        start_date_dict = {}
        start_date_dict["min_temp"] = tmin
        start_date_dict["avg_temp"] = tavg
        start_date_dict["max_temp"] = tmax
        start_date_results.append(start_date_dict)

    return jsonify(start_date_results)
    
    
@app.route("/api/v1.0/<start_date>/<end_date>")
def startend(start_date, end_date):
# Create our session (link) from Python to the DB
    session = Session(engine)
    start_end_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()   
    session.close()

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    start_end_results = []
    for tmin, tavg, tmax in start_end_query:
        start_end_dict = {}
        start_end_dict["min_temp"] = tmin
        start_end_dict["avg_temp"] = tavg
        start_end_dict["max_temp"] = tmax
        start_end_results.append(start_end_dict)

    return jsonify(start_end_results)

if __name__ == '__main__':
    app.run(debug=True)