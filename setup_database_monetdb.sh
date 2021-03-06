#!/bin/bash

ssb_config="ssb.config.json"
data_folder=`python -c "import sys, json; print(json.load(open(\"${ssb_config}\"))['data-folder'])"`
scale_factor=`python -c "import sys, json; print(json.load(open(\"${ssb_config}\"))['scale-factor'])"`

# get config info from the monetdb config file
monetdb_config="monetdb.config.json"
dbfarm_location=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['dbfarm-location'])"`
port=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['port'])"`
log_name=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['log-name'])"`
database_name=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['database-name'])"`

# reset the data generation
rm -r $data_folder

# create the MonetDB database setup
# need -r to recreate tables in monetdb
# need -k to keep the raw load data around
./scripts/setup-ssb-db -r -s $scale_factor -l $log_name -d $database_name -f $dbfarm_location -p $port -k -D $data_folder
