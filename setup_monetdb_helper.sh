#!/bin/bash

data_folder="/scratch1/leilani/code/ssb-tools-fork/generated_data"
# uses monetdb user credentials
export DOTMONETDBFILE="setup/monetdb/.monetdb"

# locate the monetdb configuration file
monetdb_config="monetdb.config.json"
# get the location to put the dbfarm
database_name=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['database-name'])"`

# create the tables
mclient -d $database_name < createTables.sql

# load the data
#COPY INTO customer  from 'PWD/customer.tbl'   USING DELIMITERS '|', '|\n';
mclient -d $database_name  -s "COPY INTO customer from '${data_folder}/customer.tbl' USING DELIMITERS '|', '|\n';"

#COPY INTO date_     from 'PWD/date.tbl'       USING DELIMITERS '|', '|\n';
mclient -d $database_name  -s "COPY INTO date_ from '${data_folder}/date.tbl' USING DELIMITERS '|', '|\n';"
#COPY INTO part      from 'PWD/part.tbl'       USING DELIMITERS '|', '|\n';
mclient -d $database_name  -s "COPY INTO part from '${data_folder}/part.tbl' USING DELIMITERS '|', '|\n';"
#COPY INTO supplier  from 'PWD/supplier.tbl'   USING DELIMITERS '|', '|\n';
mclient -d $database_name  -s "COPY INTO supplier from '${data_folder}/supplier.tbl' USING DELIMITERS '|', '|\n';"
#COPY INTO lineorder from 'PWD/lineorder.tbl'  USING DELIMITERS '|', '|\n';
mclient -d $database_name  -s "COPY INTO lineorder from '${data_folder}/lineorder.tbl' USING DELIMITERS '|', '|\n';"
