# using run-workflow.sh with DuckDB
To run SSB using the main bash script and DuckDB, run the following in the root repository folder (i.e., the `ssb-tools-fork` root folder):
```
./run-workflow.sh [env folder location] duckdb [result destination]
```

Example:
```
./run-workflow.sh ../env duckdb results/test
```

NOTE: this script assumes you are using a virtual environment to run Python with SSB. "env folder location" refers to the location of the Python virtual environment setup for running SSB.

NOTE: starting/stopping the database doesn't actually do anything with DuckDB, so you can ignore these scripts (included just so the execution flow is consistent for the `run-workflow.sh` script).

# Using the DuckDB scripts
There is a bash script saved in this folder (`setup/duckdb`) for basic things that need to be done for DuckDB. To run any of these scripts, simply run them directly in the root folder of the ssb-tools-fork repository:
```
./setup/duckdb/[scriptname].sh
```

To run the experiments with SSB and DuckDB, you will need the `duckdb` Python connector.

An example of how to run experiments using DuckDB with the benchmark using SSB directly (using the root repository folder):
```
python run_benchmark_queries.py --driver-name duckdb
```

# Experiment flow
In general, all of the following steps should be carried out to have a clean run with DuckDB. The following sections explains each of the scripts.
1. run SSB

Note that DuckDB doesn't have any setup/teardown requirements, so we do not have to do start/stop of the database. These scripts only exist for consistency's sake.

# Refreshing the DuckDB Databaes and Reloading Datasets
There is one script to load data of any scale factor: `load-ssb-data.sh`. Scale factor is specified in the `ssb.config.json` file in the root director. However, the scripts assume you have already generated the data of the appropriate scale factor (using the `generate_data.sh` script). You can run this script directly as follows:
```
./setup/duckdb/load-ssb-data.sh
```
