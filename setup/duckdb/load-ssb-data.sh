#!/bin/bash

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"

ssb_config="${root_dir}/ssb.config.json"
data_folder=`python -c "import sys, json; print(json.load(open(\"${ssb_config}\"))['data-folder'])"`
scale_factor=`python -c "import sys, json; print(json.load(open(\"${ssb_config}\"))['scale-factor'])"`

# locate the monetdb configuration file
duckdb_config="${root_dir}/duckdb.config.json"
# get the location to put the dbfarm
dbFilename=`python -c "import sys, json; print(json.load(open(\"${duckdb_config}\"))['dbFilename'])"`
rm $dbFilename

# will make the database in the current folder
#python setup/duckdb/load_1M.py "${root_dir}/crossfilter-eval-db.duckdb"
python ${current_dir}/load-ssb-data.py ${duckdb_config} ${ssb_config}
