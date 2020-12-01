import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

## Database Engine Structure ##
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
#Base.classes.keys()

S = Base.classes.station
M = Base.classes.measurement

min_pull = func.min(M.tobs)
max_pull = func.max(M.tobs)
avg_pull = func.avg(M.tobs)

## APP STRUCTURE ##
app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Welcome to the Hawaiian Weather Collection Database API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"For start date only:<br/>"
        f"/api/v1.0/start_date/<start><br/>"
        f"<br/>"
        f"For start and end date (Start date first, End date second):<br/>"
        f"/api/v1.0/start_date/yyyy-mm-dd/end_date/yyyy-mm-dd<br/>"
    )

@app.route("/api/v1.0/precipitation")
def percip_page():
    session = Session(engine)

    p_r = session.query(M.date, M.prcp).all()

    session.close()

    perc_list = []
    for date, prcp in p_r:
        percip_dict = {}
        percip_dict["date"] = date
        percip_dict["prcp"] = prcp
        perc_list.append(percip_dict)
    
    return jsonify(perc_list)

@app.route("/api/v1.0/stations")
def stations_page():
    session = Session(engine)

    st_data = session.query(S.name, S.station, S.latitude, S.longitude, S.elevation).all()

    session.close()

    stations_list = []
    for name, station, latitude, longitude, elevation in st_data:
        station_dict = {}
        station_dict["name"] = name
        station_dict["station_ID"] = station
        station_dict["lat"] = latitude
        station_dict["lon"] = longitude
        station_dict["elevation"] = elevation
        stations_list.append(station_dict)
    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def freq_tobs():
    session = Session(engine)

    freq_count = func.count(M.station)

    most_freq = session.query(M.station, freq_count).group_by(M.station).order_by(freq_count.desc()).first()
    most_freq_stn = most_freq[0]

    freq_year_pull = session.query(M.date, M.station, M.tobs).\
    filter(M.date > '2016-08-23').\
    filter(M.station == most_freq_stn).\
    order_by(M.date).all()

    session.close()

    freq_list = []
    for date, station, tobs in freq_year_pull:
        freq_dict = {}
        freq_dict["date"] = date
        freq_dict["station"] = station
        freq_dict["temp_recorded"] = tobs
        freq_list.append(freq_dict)

    return jsonify(freq_list)


@app.route("/api/v1.0/start_date/<start>")
def start_only(start):
    try:
        session = Session(engine)
        
        start_data = session.query(min_pull, avg_pull, max_pull).\
            filter(M.date >= str(start))
        
        session.close()

        start_list = []
        for s_min, s_avg, s_max, in start_data:
            start_dict = {}
            start_dict['tmin'] = s_min
            start_dict['tavg'] = s_avg
            start_dict['tmax'] = s_max
            start_list.append(start_dict)
        
        if s_avg is None:
            return print(f"Date not in Database, please try another date")
        else:
            return jsonify(start_list)
    except TypeError:
        return print(f"Date not in Database, please try another date")

@app.route("/api/v1.0/start_date/<start>/end_date/<end>")
def calc_temps(start, end):
    try:
        session = Session(engine)

        end_data = session.query(min_pull, avg_pull, max_pull).\
            filter(M.date >= str(start)).\
            filter(M.date <= str(end)).all()
    
        session.close()

        end_list = []
        for e_min, e_avg, e_max, in end_data:
            end_dict = {}
            end_dict['tmin'] = e_min
            end_dict['tavg'] = e_avg
            end_dict['tmax'] = e_max
            end_list.append(end_dict)

        if e_avg is None:
            return print(f"One or more date is not in Database, please try another date range")
        else:
            return jsonify(end_list)
    except TypeError:
        return print(f"One or more date is not in Database, please try another date range")

#Run App
if __name__ == "__main__":
    app.run(debug=False)