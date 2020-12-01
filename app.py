from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np

## Database Engine Structure ##
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

S = Base.classes.station
M = Base.classes.measurement

## APP STRUCTURE ##
app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Welcome to the Hawaiian Weather Collection Database API<br/>"
        f"Available Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitations")
def percip():
    session = Session(engine)

    percip_r = session.query()

#@app.route("/api/v1.0/stations")

#@app.route("/api/v1.0/tobs")

#@app.route("/api/v1.0/<start>")

#@app.route("/api/v1.0/<start>/<end>")

if __name__ == "__main__":
    app.run(debug=True)