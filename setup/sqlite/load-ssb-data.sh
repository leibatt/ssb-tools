#!/bin/bash

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"

ssb_config="${root_dir}/ssb.config.json"
data_folder=`python -c "import sys, json; print(json.load(open(\"${ssb_config}\"))['data-folder'])"`
scale_factor=`python -c "import sys, json; print(json.load(open(\"${ssb_config}\"))['scale-factor'])"`

# locate the monetdb configuration file
sqlite_config="${root_dir}/sqlite.config.json"
# get the location to put the dbfarm
dbFilename=`python -c "import sys, json; print(json.load(open(\"${sqlite_config}\"))['dbFilename'])"`

if [ -f $dbFilename ] ; then
    rm $dbFilename
fi

# will make the database in the current folder
echo "python ${current_dir}/load-ssb-data.py ${sqlite_config} ${ssb_config}"
python ${current_dir}/load-ssb-data.py ${sqlite_config} ${ssb_config}
