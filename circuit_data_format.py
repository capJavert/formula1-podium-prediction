import pandas as pd

circuits = pd.read_csv('data/circuits.csv', sep=',', encoding='latin-1')
finishes = pd.read_csv('data/driverStandings.csv', sep=',', encoding='utf8')
races = pd.read_csv('data/races.csv', sep=',', encoding='latin-1')
drivers = pd.read_csv('data/drivers.csv', sep=',', encoding='latin-1')

circuit_data_by_year = {}

for year in range(2000, 2017):
    for _, circuit in circuits.iterrows():
        for _, race in races[(races["circuitId"] == circuit["circuitId"]) & (races["year"] == year)].iterrows():
            circuit_data_by_year[str(circuit["circuitId"]) + "-" + str(year)] = finishes[finishes["raceId"] == race["raceId"]]

for name, data_set in circuit_data_by_year.items():
    del data_set["driverStandingsId"]
    del data_set["wins"]
    del data_set["positionText"]
    del data_set["points"]

    data_set.to_csv("data/circuits/" + name + ".csv", sep=',', encoding='latin-1', index=False)
