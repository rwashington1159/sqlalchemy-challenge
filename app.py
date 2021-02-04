import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

######################################################################

engine = create_engine("sqlite:///hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#########################################################################

#Create an app
from flask import Flask

app = Flask(__name__)

#Define what to do when user hits index route

@app.route("/")
def home():
    """List all routes that are available."""
    return(
    f"Welcome to the Hawaii Climate Analysis!"
    "<br/v>"
    f"Available Routes: <br/>"
    f"<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"<br/>"
    f"/api/v1.0/stations"
    f"<br/v>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start>"
    f"/api/v1.0/min_max_avg/&lt;start date&gt;/&lt;end date&gt;<br/>"
    f"<br/>;"
)

# Create precipitation route 
# 'def' is defining a function which is precipitation in this case

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    precipitation = []
    for result in results:
        r = {}
        r[result[0]] = result[1]
    precipitation.append(r)

    session.close()

    return jsonify(precipitation)
# a function will always have something on return which is the output


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    stations = {}

    results = session.query(Station.station, Station.name).all()
    for s, name in results:
        stations[s] = name

    session.close()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    oneyr_ago = (dt.datetime.strptime(last_date[0], '%Y-%m-%d')\
                    -dt.timedelta(days=365)).strftime('%Y-%m-%d')

    results = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= oneyr_ago).\
                order_by(Measurement.date).all()

    tobs_date_list = []

    for date, tobs in results:
        new_dict = {}
        new_dict[date] = tobs
        tobs_date_list.append(new_dict)

    session.close()

    return jsonify(tobs_date_list)

# you can pass inputs inside a func "<start> will be a user input"
@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)

    start_weather = []

    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >=start).all()
    for min_temp, max_temp, avg_temp in results:
        start = {}
        start["min_temp"] = min_temp
        start["max_temp"] = max_temp
        start["avg_temp"] = avg_temp
        start_weather.append(start)


    session.close()

    return jsonify(start_weather)


if __name__ == "__main__":
    app.run(debug=True)