Code for the SSB, forked from the following GitHub Project:
```
https://github.com/eyalroz/ssb-tools/
```

You will need to make sure the associated SSB `dbgen` github repository is also cloned, and located in the `dbgen` folder of this project:
```
https://github.com/eyalroz/ssb-dbgen/
  echo "Example: ./run-all-workflows-all-drivers.sh ../env 1"
```

The structure of this benchmark is very similar to the `crossfilter` benchmark. The benchmark is configured using the .config files located within the root directory (`monetdb.config.json`, `duckdb.config.json`, etc.). A master config file is located at `ssb.config.json`.

This script takes a virtual environment (Python 3) and number of runs per DBMS (default: 1).

The benchmark assumes that the active user has permissions to setup and run each DBMS. Helpful setup scripts for each DBMS are located in the setup folder. Please complete setup prior to running this version of the SSB. Note that these scripts were adapted from the `crossfilter` benchmark.

To run this SSB benchmark, please make sure `ssb.config.json` is properly configured, then run:
```
./run-all-workflows-all-drivers.sh
```

This script will handle generation of the data using dbgen, loading of the data into each DBMS, generation of queries for the given dataset scale factor, and execution of the generated queries on each DBMS in a randomized order, for a given number of runs per DBMS. If you want to modify which DBMSs get run, then edit line 127 in the `run-all-workflows-all-drivers.sh` script. If you want to ignore VerdictDB, then comment out the code from line 86 to line 124 of the script.

This script will generate output in the results folder. Then `getDurations.py` from the analysis folder can be run to produce a report of the execution results.
