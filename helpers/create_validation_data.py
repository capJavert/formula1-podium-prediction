import pandas as pd

circuits = pd.read_csv('../data/circuits.csv', sep=',', encoding='latin-1')
finishes = pd.read_csv('../data/driverStandings.csv', sep=',', encoding='utf8')
races = pd.read_csv('../data/racesNew.csv', sep=',', encoding='latin-1')
drivers = pd.read_csv('../data/drivers.csv', sep=',', encoding='latin-1')
lap_times = pd.read_csv('../data/lapTimesNew.csv', sep=',', encoding='utf8')
qualifications = pd.read_csv('../data/qualifyingFormated.csv', sep=',', encoding='utf8')

columns = [
    'driverId',
    'raceId',
    'morning_line',  # qualifications result
    'winner',
    'podium',
    'fastest_lap',
    'podium_percent',
    'win_percent',
    'previous_winner',
    'recent_winner',
    'position'
]

circuit_data_by_year = {}
validation_set = pd.DataFrame(columns=columns)

for year in range(2017, 2018):
    for _, circuit in circuits.iterrows():
        for _, race in races[(races["circuitId"] == circuit["circuitId"]) & (races["year"] == year)].iterrows():
            circuit_data_by_year[str(circuit["circuitId"]) + "-" + str(year)] = finishes[
                finishes["raceId"] == race["raceId"]]

for _, driver in drivers.iterrows():
    print(driver["driverId"])
    last_place = 0
    last_win = 0
    wins = 0
    podiums = 0
    race = 0

    for _, circuit_data in circuit_data_by_year.items():
        for _, data_set in circuit_data.iterrows():
            if data_set["driverId"] != driver["driverId"]:
                continue

            race += 1

            # je pobjedio = 1 else 0
            # u postolju = 1 else 0
            driver_stats = {
                'driverId': driver["driverId"],
                'raceId': data_set["raceId"],
                'winner': 1 if data_set["position"] == 1 else 0,
                'podium': 1 if data_set["position"] <= 3 else 0,
                'position': data_set["position"]
            }

            # qualifikacijski rezultat
            qualification_result = qualifications[
                (qualifications["raceId"] == data_set["raceId"]) & (qualifications["driverId"] == driver["driverId"])]
            if not qualification_result.empty:
                driver_stats["morning_line"] = qualification_result.iloc[0]["odds"]
            else:
                driver_stats["morning_line"] = "0-1"

            # nabrži krug = 1 else 0
            fastest_driver = lap_times[lap_times["raceId"] == data_set["raceId"]]["milliseconds"].idxmax()
            driver_stats['fastest_lap'] = 1 if driver["driverId"] == lap_times.iloc[fastest_driver]["driverId"] else 0

            # postotak postolja > 50% = 1 else 0
            if data_set["position"] <= 10:
                podiums += 1
            driver_stats["podium_percent"] = 1 if podiums / race * 100 > 50 else 0

            # postotak pobjeda > 50% = 1 else 0
            if driver_stats["winner"] == 1:
                wins += 1
            driver_stats["win_percent"] = 1 if wins / race * 100 > 50 else 0

            # vozac pobjedio zadnju utrku = 1 else 0
            driver_stats["previous_winner"] = 1 if last_place == 1 else 0

            # vozac pobjedio u zadnje tri utrke = 1 else 0
            driver_stats["recent_winner"] = 1 if race - last_win <= 10 and last_win != 0 else 0

            last_place = data_set["position"]

            if driver_stats["winner"] == 1:
                last_win = race

            rows = []
            for col in columns:
                rows.append(driver_stats[col])

            validation_set.loc[len(validation_set)] = rows

validation_set.to_csv("../data/validation_set-02.csv", sep=',', encoding='latin-1', index=False)
