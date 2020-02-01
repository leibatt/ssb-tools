#!/bin/bash

# locate the root directory
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"
current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

ssb_config="${root_dir}/ssb.config.json"
data_folder=`python -c "import sys, json; print(json.load(open(\"${ssb_config}\"))['data-folder'])"`
scale_factor=`python -c "import sys, json; print(json.load(open(\"${ssb_config}\"))['scale-factor'])"`

# locate the monetdb configuration file
postgres_config="${root_dir}/postgresql.config.json"
psql_loc=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['psql_loc'])"`
password=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['password'])"`
port=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['port'])"`
database_name=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['database-name'])"`
username=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['username'])"`

# uses specified user credentials
export PGPASSWORD=$password
$psql_loc -U ${username} --host=localhost -p $port -d $database_name < ${current_dir}/createTablesPostgresql.sql

$psql_loc -U ${username} --host=localhost -p $port -d $database_name -c "\\copy customer from '${data_folder}/sf_${scale_factor}/customer.tbl' DELIMITER '|' NULL '';"
$psql_loc -U ${username} --host=localhost -p $port -d $database_name -c "ALTER TABLE customer  DROP COLUMN extra;"

$psql_loc -U ${username} --host=localhost -p $port -d $database_name -c "\\copy date_ from '${data_folder}/sf_${scale_factor}/date.tbl' DELIMITER '|' NULL '';"
$psql_loc -U ${username} --host=localhost -p $port -d $database_name -c "ALTER TABLE date_  DROP COLUMN extra;"

$psql_loc -U ${username} --host=localhost -p $port -d $database_name -c "\\copy part from '${data_folder}/sf_${scale_factor}/part.tbl' DELIMITER '|' NULL '';"
$psql_loc -U ${username} --host=localhost -p $port -d $database_name -c "ALTER TABLE part  DROP COLUMN extra;"

$psql_loc -U ${username} --host=localhost -p $port -d $database_name -c "\\copy supplier from '${data_folder}/sf_${scale_factor}/supplier.tbl' DELIMITER '|' NULL '';"
$psql_loc -U ${username} --host=localhost -p $port -d $database_name -c "ALTER TABLE supplier  DROP COLUMN extra;"

$psql_loc -U ${username} --host=localhost -p $port -d $database_name -c "\\copy lineorder from '${data_folder}/sf_${scale_factor}/lineorder.tbl' DELIMITER '|' NULL '';"
$psql_loc -U ${username} --host=localhost -p $port -d $database_name -c "ALTER TABLE lineorder  DROP COLUMN extra;"
