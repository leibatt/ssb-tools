#!/bin/bash

# locate the root directory
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"
# locate the monetdb configuration file
postgres_config="${root_dir}/postgresql.config.json"
# get the location to put the dbfarm
psql_loc=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['psql_loc'])"`
password=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['password'])"`
port=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['port'])"`
database_name=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['database-name'])"`
username=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['username'])"`

postgres_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../postgresql" >/dev/null 2>&1 && pwd )"
$psql_loc -p $port -d $database_name -c "create user ${username} with password '${password}';"
$psql_loc -p $port -d $database_name -c "grant all privileges on database \"$database_name\" to ${username};"
