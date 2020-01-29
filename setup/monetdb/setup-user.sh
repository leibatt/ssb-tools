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

mclient -d $database_name  -s "CREATE USER ${username} WITH PASSWORD '${password}' NAME '${username}' SCHEMA sys;"
mclient -d $database_name  -s "grant all privileges on sys.customer to ${username};"
mclient -d $database_name  -s "grant all privileges on sys.date_ to ${username};"
mclient -d $database_name  -s "grant all privileges on sys.part to ${username};"
mclient -d $database_name  -s "grant all privileges on sys.supplier to ${username};"
mclient -d $database_name  -s "grant all privileges on sys.lineorder to ${username};"
