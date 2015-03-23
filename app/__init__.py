'''
initalize Flask app
'''
from flask import Flask
import os

app = Flask('app')
app.config.from_object('config')

# Pull in URL dispatch routes
from app import views