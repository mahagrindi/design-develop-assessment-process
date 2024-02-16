from flask import Flask
from dotenv import load_dotenv

#************************************#
#********* Loading env file *********#
#************************************#
load_dotenv()

#************************************#
#********* Creating app *************#
#************************************#
app = Flask(__name__)

#************************************#
#********* Importing routes *********#
#************************************#
from controllers.ScrapperController import *