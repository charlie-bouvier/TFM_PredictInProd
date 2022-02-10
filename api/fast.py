from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import joblib
import pandas as pd
from datetime import datetime
import pytz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")


def predict(pickup_datetime,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count):
        # localize the user datetime with NYC timezone
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)

    # localize the datetime to UTC
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")

    params={
    "key":['2013-07-06 17:18:00.000000119'],
    "pickup_datetime": [formatted_pickup_datetime],
    "pickup_longitude": [float(pickup_longitude)],
    "pickup_latitude": [float(pickup_latitude)],
    "dropoff_longitude": [float(dropoff_longitude)],
    "dropoff_latitude": [float(dropoff_latitude)],
    "passenger_count": [int(passenger_count)]
    }
    pipeline = joblib.load("model.joblib")
    df=pd.DataFrame.from_dict(params)
    fare=pipeline.predict(df)
    return {"Fare": fare[0]}
    # response = requests.get(params).json()





# pickup_datetime = "2021-05-30 10:12:00"
