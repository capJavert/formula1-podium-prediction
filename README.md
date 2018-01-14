# Formula 1 Podium Prediction

## The code

To run this demo, you will need:

- Python 3.x
- Pip
- Sklearn
- Scipy
- Numpy
- pandas (only for further data formatting and science)

### Setup the code
```
$ git clone https://github.com/capJavert/formula1-podium-prediction.git
$ sudo pip install numpy
$ sudo pip install scipy
$ sudo pip install sklearn
$ sudo pip install pandas
$ sudo pip install -r requirements.txt
```

### Training the model
```
$ python f1-trainer.py
```
- model is written to f1-finish_pos.model file for further reuse

### Running GUI application
- web application runs on localhost:8080
- **(optional)** allow connections in your firewall settings
```
$ python run.py
```
