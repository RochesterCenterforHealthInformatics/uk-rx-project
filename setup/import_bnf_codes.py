import csv
import sqlalchemy
import time
import datetime
from MySQLdb import escape_string
import configparser
import helper


config_file = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file)

period = '201803'
file = 'data/BNF_Code_Information.csv'

# Breaking down BNF code information into separate tables for easy data wrangling

bnf_full_sql = 'insert into bnf_code_full (bnf_code, name) values '
bnf_full_values_sql = helper.make_values_sql(2)

bnf_chapter_sql = 'insert into bnf_chapter (bnf_code_2, name) values '
bnf_chapter_values_sql = helper.make_values_sql(2)

bnf_section_sql = 'insert into bnf_section (bnf_code_4, name) values '
bnf_section_values_sql = helper.make_values_sql(2)

bnf_name_sql = 'insert into bnf_code_9 (bnf_code_9, name) values '
bnf_values_sql = helper.make_values_sql(2)

buffer_size = 5000  # higher value will increase insertion speed

try:
    engine = sqlalchemy.create_engine(config['DEFAULT']['uri'], pool_recycle=3600)
    db = engine.connect()
except Exception:
    print("Can't connect to database")
    exit()

print("\nPopulating BNF Code information...")
with open(file) as csvfile:
    f = csv.reader(csvfile, delimiter=',')
    start_time = time.time()
    counter = 0
    bufferB = {}
    bufferC = {}
    bufferD = {}
    sqlB = bnf_chapter_sql
    sqlC = bnf_section_sql
    sqlD = bnf_name_sql

    for i, row in enumerate(f, start=1):
        if counter == 0:
            sqlA = bnf_full_sql

        if i != 1:
            if counter:
                sqlA = sqlA + ', '
            name_full = escape_string(row[12].strip()).decode("utf-8").replace("%", "%%")
            sqlA = sqlA + bnf_full_values_sql.format(row[13], name_full)

            if not row[1] in bufferB:
                if bufferB.__len__():
                    sqlB = sqlB + ', '
                bufferB[row[1]] = escape_string(row[0].strip()).decode("utf-8").replace("%", "%%")
                sqlB += bnf_chapter_values_sql.format(row[1], bufferB[row[1]])

            if not row[3] in bufferC:
                if bufferC.__len__():
                    sqlC = sqlC + ', '
                bufferC[row[3]] = escape_string(row[2].strip()).decode("utf-8").replace("%", "%%")
                sqlC += bnf_section_values_sql.format(row[3], bufferC[row[3]])

            if not row[9] in bufferD:
                if bufferD.__len__():
                    sqlD = sqlD + ', '
                bufferD[row[9]] = escape_string(row[8].strip()).decode("utf-8").replace("%", "%%")
                sqlD += bnf_values_sql.format(row[9], bufferD[row[9]])

            counter += 1

        if counter == buffer_size:
            counter = 0
            db.execute(sqlA)

        if i % 25000 == 0:
            end_time = time.time()
            uptime = end_time - start_time
            human_uptime = str(datetime.timedelta(seconds=int(uptime)))
            rate = round(i / uptime)
            print(f'Record num: {i}')
            print(f'Time elapsed: {human_uptime}')
            print(f'Insert rate: {rate} records/sec')

    if counter:
        db.execute(sqlA)
        db.execute(sqlB)
        db.execute(sqlC)
        db.execute(sqlD)

    end_time = time.time()
    uptime = end_time - start_time
    human_uptime = str(datetime.timedelta(seconds=int(uptime)))
    rate = round(i / uptime)
    print(f'Total Record num: {i - 1}')
    print(f'Total Time elapsed: {human_uptime}')
    print(f'Avg Insert rate: {rate} records/sec')

db.close()
