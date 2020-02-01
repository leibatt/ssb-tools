# using run-workflow.sh with MonetDB
To run SSB using the main bash script and MonetDB, run the following in the root repository folder (i.e., the `ssb-tools-fork` root folder):
```
./run-workflow.sh [env folder location] monetdb [result destination]
```

Example:
```
./run-workflow.sh ../env monetdb results/test
```

NOTE: you can configure MonetDB using the `monetdb.config.json` file in the root repository folder (i.e., the `ssb-tools-fork` root folder)

NOTE: this script assumes you are using a virtual environment to run Python with SSB. "env folder location" refers to the location of the Python virtual environment setup for running SSB.

NOTE: this does not start and stop the dbfarm, and it does not finally stop the database! these steps should be handled either manually or using a larger script that processes multiple workflows...

# Using the MonetDB scripts
There is a bash script saved in this folder (`setup/monetdb`) for anything that needs to be done with MonetDB. To run any of these scripts, simply run them directly in the root folder of this repository:
```
./setup/monetdb/[scriptname].sh
```

For example, to reset the ssb-test database (assuming the dbfarm has been created already):
```
./setup/monetdb/reset-database.sh
```

To run the experiments with SSB and MonetDB, you will need the MonetDB Python connector: `pymonetdb`.

An example of how to run experiments using MonetDB with the benchmark (using the root repository folder):
```
python run_benchmark_queries.py --driver-name monetdb
```

# Experiment flow
In general, all of the following steps should be carried out to have a clean run with MonetDB. These steps assume that the dbfarm has already been created. The following sections explains each of the scripts.
1. [once] start the dbfarm (using `start-dbfarm.sh`)
2. [once] reset the database (using `reset-database.sh`)
3. [once] load the data (e.g., use `load-ssb-data.sh`)
4. stop the database (using `stop-database.sh`)
5. start the database (using `start-database.sh`)
6. run SSB for the given workflow
7. [once] stop the database one final time (using `stop-database.sh`)
8. [once] stop the dbfarm (using `stop-dbfarm.sh`)

Note that steps 1, 2, and 3 need to be performed once before all experiments, and steps 7 and 8 once after all experiments are done.

# Starting, Stopping (and if necessary Creating) the MonetDB DBFarm
MonetDB needs a dbfarm first, to manage multiple databases. If you need to create one, this can be done using the `create-dbfarm.sh` script, which will create the dbfarm:
```
./setup/monetdb/create-dbfarm.sh
```

After creating the dbfarm, then you need to start it, which you can use the `start-dbfarm.sh` script:
```
./setup/monetdb/start-dbfarm.sh
```

After running expeirments, you need to stop the dbfarm using the `stop-dbfarm.sh` script:
```
./setup/monetdb/stop-dbfarm.sh
```

# Setting Up, Starting, and Stopping the Crossfilter Database
Once the dbfarm is up and running, then we need a database to run experiments with. You can create the ssb-test database using the `create-database.sh` script:
```
./setup/monetdb/create-database.sh
```

Once we have the database, we can start it using `start-database.sh`:
```
./setup/monetdb/start-database.sh
```

As a shortcut, you can quickly re-create the database from scratch using the `reset-database.sh`:
```
./setup/monetdb/reset-database.sh
```

To stop the database after running experiments, we can use `stop-database.sh`:
```
./setup/monetdb/stop-database.sh
```

# Loading Datasets
There is one script to load data of any scale factor: `load-ssb-data.sh`. Scale factor is specified in the `ssb.config.json` file in the root director. However, the scripts assume you have already generated the data of the appropriate scale factor (using the `generate_data.sh` script). You can run this script directly as follows:
```
./setup/monetdb/load-ssb-data.sh
```
