#!/bin/bash

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"
# uses monetdb user credentials
export DOTMONETDBFILE="${current_dir}/.monetdb"

# locate the monetdb configuration file
monetdb_config="${root_dir}/monetdb.config.json"
# get the location to put the dbfarm
database_name=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['database-name'])"`
password=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['password'])"`
username=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['username'])"`


monetdb create ${database_name}
monetdb release ${database_name}

