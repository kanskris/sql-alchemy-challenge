#import flask and jsonify
from flask import Flask, jsonify

#import all the stuuf we imported on starter pack
from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

#default route
@app.route("/")
def welcome():
    return (
        f"Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/2012-12-12<br/>"
        f"/api/v1.0/temp/2012-12-12/2013-01-02"
    )

#precipitation route
@app.route("/api/v1.0/precipitation")
def precp_analysis():
    #use the same code from python but covert the data to json and return
    year_start = dt.date(2017,8,23)-dt.timedelta(days=365)
    precp_analysis = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_start).all()
    precp_flask ={date: prcp for date, prcp in precp_analysis}
    return jsonify(precp_flask)

#station route
@app.route("/api/v1.0/stations")
def stations():
    #use the same code from python but covert the data to json and return    
    stations = session.query(Station.station, Station.name).all()
    stations_flask = {station: name for station, name in stations}
    return jsonify(stations_flask)

#tobs route    
@app.route("/api/v1.0/tobs")
def tobs():
    #use the same code from python but covert the data to json and return
    year_start = dt.date(2017,8,23)-dt.timedelta(days=365)
    high_station_analysis=session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= year_start).all()
    tobs_flask = {date:tobs for date,tobs in high_station_analysis}
    return jsonify(tobs_flask)

#start date route
@app.route("/api/v1.0/temp/<start_date>")
def diff_temp_greaterthan(start_date):
    #use the same code from python but covert the data to json and return
    diff_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    return jsonify(diff_temp)

#start date and end date route
@app.route("/api/v1.0/temp/<start_date>/<end_date>")
def diff_temp_range(start_date, end_date):
    #use the same code from python but covert the data to json and return
    diff_temp=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(diff_temp)

if __name__ == '__main__':
    app.run()