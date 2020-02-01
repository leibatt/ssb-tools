#!/bin/bash

# locate the root directory
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"
# locate the monetdb configuration file
postgres_config="${root_dir}/postgresql.config.json"
# get the location to put the dbfarm
psql_loc=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['psql_loc'])"`
database_name=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['database-name'])"`
port=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['port'])"`
crdb="$( dirname "${psql_loc}" )/createdb"

echo "$crdb -p $port ${database_name}"
$crdb -p $port ${database_name}
