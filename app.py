from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

import flask
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():  
    """List all routes that are available"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        
    )



@app.route("/api/v1.0/precipitation")

def precipitation():
    NewData = session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()
    return jsonify(dict(NewData))

@app.route("/api/v1.0/stations")

def stations():
    StationInfo = session.query( Measurement.station , func.count(Measurement.station)).group_by( Measurement.station ).order_by(func.count(Measurement.station).desc()).all()
    return jsonify(dict(StationInfo))

@app.route("/api/v1.0/tobs")

def tobs():
    lastdata = session.query (Measurement.date).filter(Measurement.station == 'USC00519281').order_by(Measurement.date.desc()).first()
    return jsonify(dict(lastdata))

if __name__ == "__main__":
    app.run(debug = True)