import sys
import csv
import sqlalchemy
import time
import datetime
import configparser
import helper


config_file = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file)

# Flag all irrelevant prescription data

