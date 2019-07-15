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

rx_filename = 'data/practice_features.csv'
rx_file = rx_filename.format(period)

rx_prescribed_sql = 'insert into practice (org_code, name, nat_group, hlhg, addr_1, addr_2, addr_3, addr_4, addr_5, post_code, open_date, close_date, status_code, prescribing_setting, num_practitioners) values '
rx_values_sql = helper.make_values_sql(15)

buffer_size = 1000

try:
    engine = sqlalchemy.create_engine(config['DEFAULT']['uri'], pool_recycle=3600)
    db = engine.connect()
except Exception:
    print("Can't connect to database")
    exit()

print("Importing rx...")
with open(rx_file) as csvfile:
    f = csv.reader(csvfile, delimiter=',')
    start_time = time.time()
    counter = 0

    for i, row in enumerate(f, start=1):
        if counter == 0:
            sql = rx_prescribed_sql

        if i != 1:
            if counter:
                sql = sql + ', '
            sql = sql + rx_values_sql.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
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
    print(f'Total Record num: {i-1}')
    print(f'Total Time elapsed: {human_uptime}')
    print(f'Avg Insert rate: {rate} records/sec')

db.close()