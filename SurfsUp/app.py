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
Measurement = Base.classes.measurment
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
    f"Available Routes for Hawaii Weather:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
    f"/api/v1.0/<start_date format:yyyy-mm-dd]/<end_date format:yyyy-mm-dd]<br/>"

@app.route("/api/v1.0/precipitation")
def precipitation():
# Create our session (link) from Python to the DB
    session = Session(engine)

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    precipititaion_query = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').all()
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
def stations():
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

# Return a JSON list of temperature observations for the previous year.

session.close()

@app.route("/api/v1.0/[start_date format:yyyy-mm-dd]")
def start():
# Create our session (link) from Python to the DB
session = Session(engine)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

session.close()

@app.route("/api/v1.0/<start_date format:yyyy-mm-dd]/<end_date format:yyyy-mm-dd]")
def startend():
# Create our session (link) from Python to the DB
session = Session(engine)

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

session.close()