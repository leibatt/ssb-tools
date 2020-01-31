#!/bin/bash

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"

ssb_config="${root_dir}/ssb.config.json"
data_folder=`python -c "import sys, json; print(json.load(open(\"${ssb_config}\"))['data-folder'])"`
scale_factor=`python -c "import sys, json; print(json.load(open(\"${ssb_config}\"))['scale-factor'])"`

# uses monetdb user credentials
export DOTMONETDBFILE="${current_dir}/.monetdb"

# locate the monetdb configuration file
monetdb_config="${root_dir}/monetdb.config.json"
# get the location to put the dbfarm
database_name=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['database-name'])"`
username=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['username'])"`

# create the tables
mclient -d $database_name < $current_dir/../createTables.sql

# load the data
#COPY INTO customer  from 'PWD/customer.tbl'   USING DELIMITERS '|', '|\n';
mclient -d $database_name  -s "COPY INTO customer from '${data_folder}/sf_${scale_factor}/customer.tbl' USING DELIMITERS '|', '|\n';"

#COPY INTO date_     from 'PWD/date.tbl'       USING DELIMITERS '|', '|\n';
mclient -d $database_name  -s "COPY INTO date_ from '${data_folder}/sf_${scale_factor}/date.tbl' USING DELIMITERS '|', '|\n';"
#COPY INTO part      from 'PWD/part.tbl'       USING DELIMITERS '|', '|\n';
mclient -d $database_name  -s "COPY INTO part from '${data_folder}/sf_${scale_factor}/part.tbl' USING DELIMITERS '|', '|\n';"
#COPY INTO supplier  from 'PWD/supplier.tbl'   USING DELIMITERS '|', '|\n';
mclient -d $database_name  -s "COPY INTO supplier from '${data_folder}/sf_${scale_factor}/supplier.tbl' USING DELIMITERS '|', '|\n';"
#COPY INTO lineorder from 'PWD/lineorder.tbl'  USING DELIMITERS '|', '|\n';
mclient -d $database_name  -s "COPY INTO lineorder from '${data_folder}/sf_${scale_factor}/lineorder.tbl' USING DELIMITERS '|', '|\n';"

mclient -d $database_name  -s "grant all privileges on sys.customer to ${username};"
mclient -d $database_name  -s "grant all privileges on sys.date_ to ${username};"
mclient -d $database_name  -s "grant all privileges on sys.part to ${username};"
mclient -d $database_name  -s "grant all privileges on sys.supplier to ${username};"
mclient -d $database_name  -s "grant all privileges on sys.lineorder to ${username};"
