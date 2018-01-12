import pandas as pd

races = pd.read_csv('data/racesAll.csv', sep=',', encoding='latin-1')
qualifications = pd.read_csv('data/qualifying.csv', sep=',', encoding='utf8')

columns = [
    'raceId',
    'driverId',
    'position',
    'odds'
]

qualification_data = pd.DataFrame(columns=columns)

for _, race in races.iterrows():
    race_qualifications = qualifications[qualifications["raceId"] == race["raceId"]]
    for _, qualification in race_qualifications.iterrows():
        driver_stats = {
            'raceId': qualification["raceId"],
            'driverId': qualification["driverId"],
            'position': qualification["position"],
            'odds': str(len(race_qualifications))+"-"+str(qualification["position"])
        }

        rows = []
        for col in columns:
            rows.append(driver_stats[col])

        qualification_data.loc[len(qualification_data)] = rows

qualification_data.to_csv("data/qualifyingFormated.csv", sep=',', encoding='latin-1', index=False)
