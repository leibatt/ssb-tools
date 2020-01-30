data_folder="/scratch1/leilani/code/ssb-tools-fork/generated_data"

# get config info from the monetdb config file
monetdb_config="monetdb.config.json"
dbfarm_location=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['dbfarm-location'])"`
port=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['port'])"`
log_name=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['log-name'])"`
database_name=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['database-name'])"`
scale_factor=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['scale-factor'])"`

rm -r $data_folder

./run_dbgen.sh -r --scale-factor $scale_factor -l $log_name -d $database_name -f $dbfarm_location -p $port -k -D $data_folder
