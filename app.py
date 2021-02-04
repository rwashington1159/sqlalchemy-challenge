import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

######################################################################3

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#########################################################################33

#Create an app
from flask import Flask

app = Flask(__name__)

#Define what to do when user hits index route

@app.route("/")
def home():
    """List all routes that are available."""
    return(
    f"Welcome to the Hawaii Climate Analysis"
    f"Available Routes: <br/>"
    f"<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"<br/>"
    f"/api/v1.0/stations"
    f"<br/v>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start>; /api/v1.0/<start>/<end>"
    f"/api/v1.0/min_max_avg/&lt;start date&gt;/&lt;end date&gt;<br/>"
    f"<br/>;"
)

# Create precipitation route 
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    precipitation = []
    for result in results:
        r = {}
        r[result[0]] = result[1]
    precipitation.append(r)

    return jsonify(precipitation)

if __name__ == "__main__":
    app.run(debug=True)