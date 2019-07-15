## UK Project: Analysis of UK Providers Prescribing Patterns

### Data setup

Download the following data files:

1. GP Practice and prescribing data can be acquired from: [NHS Digital](https://data.gov.uk/dataset/176ae264-2484-4afe-a297-d51798eb8228/gp-practice-prescribing-data-presentation-level)
2. BNF Codes data from: [NHS Prescription Service](https://apps.nhsbsa.nhs.uk/infosystems/welcome)
3. UK Practice data from: []()
4. Shapefile for GeoPandas can be acquired from [Open Street Map](https://wiki.openstreetmap.org/wiki/Shapefiles)

You will need to set up a MySQL database (other SQL server works) to populate the data.

The data schema is found under `schema` folder and run the `install.sql` to initialize the database.

```bash
% mysql -u <user> -p <database> < install.sql
```

After the database is set up, import the above downloads by running a series of scripts that parse the data and populate the database for further analysis.

```bash
% cd uk-rx-project
% python data/import.py
% python data/import_bnf_codes.py
% python data/import_practices.py
% python data/import_patients_count.py
```

### Data Cleaning


### Data Transformation


### Data Exploration
