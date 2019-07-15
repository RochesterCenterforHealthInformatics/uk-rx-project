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

period = sys.argv[1] if sys.argv[1] != "" else '201801'

rx_filename = 'data/T{}PDPI BNFT.CSV'
rx_file = rx_filename.format(period)

rx_prescribed_sql = 'insert into rx_prescribed (sha_at, pct_ccg, practice, bnf_code_full, bnf_code_9, bnf_code_4, items, nic, cost, quantity, period, ignore_flag) values '
rx_values_sql = helper.make_values_sql(12)

buffer_size = 5000

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
            sql = sql + rx_values_sql.format(row[0], row[1], row[2], row[3], row[3][0:9], row[3][0:4], row[5], row[6], row[7], row[8], row[9], 0)
            counter += 1

        if counter == buffer_size:
            counter = 0
            db.execute(sql)

        if i%250000 == 0:
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
