import sys
import csv
import sqlalchemy
import time
import datetime
import configparser
import helper
from MySQLdb import escape_string


config_file = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file)

months = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08',
          'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
years = {'17':'2017', '18':'2018'}
regions = ['london', 'midlands', 'north', 'south']

base_filename = 'data/patient-count/RF2. Practice List Size and GP Count - {}{}-{}.csv'
table_columns = {'practice': 4, 'period': 9, 'gp_count': 5, 'num_patients': 8}

rx_prescribed_sql = helper.make_insert_sql('patient_count', table_columns) + ' values '
buffer_size = 500

try:
    engine = sqlalchemy.create_engine(config['DEFAULT']['uri'], pool_recycle=3600)
    db = engine.connect()
except Exception:
    print("Can't connect to database")
    exit()

for year, year_full in years.items():
    for month, month_num in months.items():
        for region in regions:
            data_file = base_filename.format(month, year, region)
            current_period = "{}{}".format(year_full, month_num)
            print("Importing {}...".format(data_file))
            with open(data_file, encoding='utf-16') as csvfile:
                f = csv.reader(csvfile, delimiter='\t')
                start_time = time.time()
                counter = 0
                e_row = {}

                for i, row in enumerate(f, start=1):
                    if counter == 0:
                        sql = rx_prescribed_sql

                    if i != 1:
                        if counter:
                            sql = sql + ', '
                        for j in range(len(row)):
                            e_row[j] = escape_string(row[j].strip()).decode("utf-8").replace("%", "%%")
                        e_row[9] = current_period;
                        sql = sql + helper.make_values_with_data(table_columns, e_row)
                        counter += 1

                    if counter == buffer_size:
                        counter = 0
                        db.execute(sql)

                    if i%1000 == 0:
                        end_time = time.time()
                        uptime = end_time - start_time
                        human_uptime = str(datetime.timedelta(seconds=int(uptime)))
                        rate = round(i/uptime)
                        print(f'Record num: {i}')
                        print(f'Time elapsed: {human_uptime}')
                        print(f'Insert rate: {rate} records/sec')

                if counter:
                    db.execute(sql)

                end_time = time.time()
                uptime = end_time - start_time
                human_uptime = str(datetime.timedelta(seconds=int(uptime)))
                rate = round(i/uptime)
                print('\n\n')
                print(f'Total Record num: {i-1}')
                print(f'Total Time elapsed: {human_uptime}')
                print(f'Avg Insert rate: {rate} records/sec')

db.close()