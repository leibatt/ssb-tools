#!/bin/bash

# get config info from the monetdb config file
monetdb_config="monetdb.config.json"
dbfarm_location=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['dbfarm-location'])"`
port=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['port'])"`
log_name=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['log-name'])"`
database_name=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['database-name'])"`
scale_factor=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['scale-factor'])"`

# create the MonetDB database setup
./scripts/setup-ssb-db -s $scale_factor -l $log_name -d $database_name -f $dbfarm_location -p $port
