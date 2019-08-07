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

rx_file = ['data/epraccur/epraccur.csv', 'data/epracarc/epracarc.csv']

table_columns = {'org_code': 0, 'name': 1, 'nat_group': 2, 'hlhg': 3, 'addr_1': 4, 'addr_2': 5, 'addr_3': 6,
                 'addr_4': 7, 'addr_5': 8, 'post_code': 9, 'open_date': 10, 'close_date': 11, 'status_code': 12,
                 'practice_setting_id': 25}

rx_prescribed_sql = helper.make_insert_sql('practice', table_columns) + ' values '
rx_values_sql = helper.make_values_sql(15)

buffer_size = 5000

try:
    engine = sqlalchemy.create_engine(config['DEFAULT']['uri'], pool_recycle=3600)
    db = engine.connect()
except Exception:
    print("Can't connect to database")
    exit()

for data_file in rx_file:
    print("Importing {}...".format(data_file))
    with open(data_file) as csvfile:
        f = csv.reader(csvfile, delimiter=',')
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
                sql = sql + helper.make_values_with_data(table_columns, e_row)
                counter += 1

            if counter == buffer_size:
                counter = 0
                db.execute(sql)

            if i%buffer_size == 0:
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