import csv
import pickle
import logging
import numpy as np
from sklearn.svm import SVR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Model(object):
    def __init__(self):
        pass

    def _get_data(self, filename):

        training_data = csv.reader(open('%s' % filename, 'r'))

        logging.info('Training Finish Position')

        y = []  # Target to train on
        X = []  # Features
        for i, row in enumerate(training_data):
            # Skip the first row since it's the headers
            if i == 0:
                continue

            # Get the target
            y.append(float(row[-1]))

            # Get the features
            data = np.array(
                [i for i in row[3:-1]]
            )
            X.append(data)

        return X, y

    def train(self):

        clf = SVR(C=1.0, epsilon=0.5, cache_size=1000, shrinking=True)
        X, y, = self._get_data('data/training_set-01.csv')

        # Fit the model
        clf.fit(X, y)

        # Pickle the model so we can save and reuse it
        s = pickle.dumps(clf)

        # Save the model to a file
        f = open('f1-finish_pos.model', 'wb')
        f.write(s)
        f.close()

    def predict(self, raceId):
        f = open('f1-finish_pos.model', 'rb')
        clf = pickle.loads(f.read())
        f.close()

        validation_data = csv.reader(
            open('data/validation_set-01.csv', 'r')
        )

        races = {}
        for i, row in enumerate(validation_data):
            if i == 0:
                continue

            race_id = int(row[1])
            finish_pos = int(row[-1])

            if race_id not in races:
                races[race_id] = []

            if finish_pos < 1:
                continue

            data = np.array([
                int(_ if len(str(_)) > 0 else 0)
                for _ in row[3:-1]
            ])
            data = data.reshape(1, -1)

            morning_line = row[2].split('-')
            morning_line = int(morning_line[0]) / int(morning_line[1])
            races[race_id].append(
                {
                    'id': int(row[0]),
                    'data': data,
                    'prediction': None,
                    'finish_pos': finish_pos,
                    'odds': morning_line
                }
            )

        for race_id, drivers in races.items():
            for driver in drivers:
                driver['prediction'] = clf.predict(
                    driver['data']
                )

        podium = []

        # drivers for race
        for driver in races[raceId]:
            if driver["prediction"] <= 4:
                podium.append(driver)

        # sort by position and return
        return sorted(podium, key=lambda k: k['prediction'])
