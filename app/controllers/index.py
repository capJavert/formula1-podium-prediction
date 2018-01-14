# -*- coding: utf-8 -*-
from app import app
from flask import render_template, request
from trainers import Model
import pandas as pd

race_data = pd.read_csv('data/racesNew.csv', sep=',', encoding='latin-1')
drivers = pd.read_csv('data/drivers.csv', sep=',', encoding='latin-1')
races = {}

for _, data in race_data.iterrows():
    races[data["raceId"]] = {"name": data["name"] + "(" + str(data["year"]) + ")", "wiki": data["url"]}


@app.route('/')
def start():
    global races
    global drivers

    if request.args.get('race') and int(request.args.get('race')) in races:
        race = int(request.args.get('race'))

        trainer = Model()
        trainer.train()
        podium = trainer.predict(race)

        for i, driver in enumerate(podium):
            meta = drivers[drivers["driverId"] == driver["id"]]
            podium[i]["name"] = meta.iloc[0]["forename"] + " " + meta.iloc[0]["surname"]
    else:
        race = None
        podium = None

    return render_template(
        'site/index.html',
        podium=podium,
        races=races,
        race=race
    )
