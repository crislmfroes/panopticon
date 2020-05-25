from flask import Flask
import os
from app.models import *
from app.auth import *
from app.blueprints import *

app = Flask(__name__)
