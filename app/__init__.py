# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
app = Flask('app')
app.config['SECRET_KEY'] = 'random'
app.debug = False
toolbar = DebugToolbarExtension(app)
from app.controllers import *
