#!/bin/bash

# get config info from the monetdb config file
#monetdb_config="monetdb.config.json"
#dbfarm_location=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['dbfarm-location'])"`
#port=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['port'])"`
#log_name=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['log-name'])"`
#database_name=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['database-name'])"`
#scale_factor=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['scale-factor'])"`
#host=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['host'])"`

# create the MonetDB database setup
#./scripts/run_benchmark_queries.sh -H $host -d $database_name -p $port

env/bin/python run_benchmark_queries.py --driver-name monetdb
#env/bin/python query_randomizer.py --driver-name monetdb
