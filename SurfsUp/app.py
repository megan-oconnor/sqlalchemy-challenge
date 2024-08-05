# Import the dependencies.
import numpy as np
from datetime import timedelta, datetime as dt

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
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"Precipitation data for one year: /api/v1.0/precipitation<br/>"
        f"Stations in dataset: /api/v1.0/stations<br/>"
        f"Temperature analysis for one year: /api/v1.0/tobs<br/>"
        f"Temperature analysis from start date (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature anaysis between two dates (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set.
    recent = session.query(Measurement).\
        order_by(Measurement.date.desc()).first()

    # Calculate the date one year from the last date in dataset.
    most_recent_entry = dt.strptime(recent.date,'%Y-%m-%d')
    year_ago = (most_recent_entry - timedelta(days=365)).strftime('%Y-%m-%d')

    # Perform a query to retrieve the data and precipitation scores
    last_year = session.query(*[Measurement.date, Measurement.prcp]).\
        filter(Measurement.date > year_ago).all()

    # Close session
    session.close()

    # Create a dictionary from the date and prcp values
    last_year_precipitation = []
    for date, prcp in last_year:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        last_year_precipitation.append(prcp_dict)

    # jsonify dictioinary
    return jsonify(last_year_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Get station list
    stations = session.query(*[Station.station, Station.name]).all()

    # Close session
    session.close()

    # Create a dictionary for the Station information
    stations_all = []
    for station, name in stations:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        stations_all.append(station_dict)

    return jsonify(stations_all)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Get the most active station for the previous year
    most_active = session.query(*[Measurement.station, func.count(Measurement.id)]).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.id).desc()).first()[0]

    # Get the dates and temperature observations for the most active station
    active_station = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active).all()

    # Create dictionary for the date and temperature observations
    list_most_active = []
    for date, tobs in active_station:
        active_dict ={}
        active_dict['date'] = date
        active_dict['temperature'] = tobs
        list_most_active.append(active_dict)

    return jsonify(list_most_active)
    

@app.route("/api/v1.0/<start>")
def start(start):
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query results
    date_results = session.query(*[func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]).\
        filter(Measurement.date >= start).all()

    # Create dictionary for results
    date_obs = []
    for min,max,avg in date_results:
        tobs_dict = {}
        tobs_dict['Lowest Temperature'] = min
        tobs_dict['Highest Temperature'] = max
        tobs_dict['Average Temperature'] = avg
        date_obs.append(tobs_dict)

    return jsonify(date_obs)

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query results
    date_results = session.query(*[func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]).\
        filter(Measurement.date >= start). filter(Measurement.date <= end).all()

    # Create dictionary for results
    date_obs = []
    for min,max,avg in date_results:
        tobs_dict = {}
        tobs_dict['Lowest Temperature'] = min
        tobs_dict['Highest Temperature'] = max
        tobs_dict['Average Temperature'] = avg
        date_obs.append(tobs_dict)

    return jsonify(date_obs)

if __name__ == '__main__':
    app.run(debug=True)