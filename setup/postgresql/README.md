# using run-workflow.sh with PostgreSQL
To run SSB using the main bash script and PostgreSQL, run the following in the root repository folder (i.e., the `ssb-tools-fork` root folder):
```
./run-workflow.sh [env folder location] postgresql [result destination]
```

Example:
```
./run-workflow.sh ../env postgresql results/test
```

NOTE: this script assumes you are using a virtual environment to run Python with SSB. "env folder location" refers to the location of the Python virtual environment setup for running SSB.

NOTE: this assumes someone already went through the trouble of setting up PostgreSQL separately (these scripts will not setup postgresql for you!)

NOTE: this does not finally stop the database! this step should be handled either manually or using a larger script that processes multiple workflows...

# Using the PostgreSQL scripts
There is a bash script saved in this folder (`setup/postgresql`) for basic things that need to be done with Postgresql. To run any of these scripts, simply run them directly in the root folder of this repository:
```
./setup/postgresql/[scriptname].sh
```

For example, to start the ssb-test database:
```
./setup/postgresql/start-database.sh
```

To run the experiments with SSB and PostgreSQL, you will need the PostgreSQL Python connector: `psycopg2`.

An example of how to run experiments using PostgreSQL with the benchmark (using the root repository folder):
```
python run_benchmark_queries.py --driver-name postgresql
```

# Experiment flow
In general, all of the following steps should be carried out to have a clean run with PostgreSQL. The following sections explains each of the scripts.
1. start the database (using `start-database.sh`)
2. load the data (e.g., `load-ssb-data.sh`)
3. stop the database (using `stop-database.sh`)
4. start the database (using `start-database.sh`)
5. run SSB
6. stop the database one final time (using `stop-database.sh`)

Note that steps 1, 2 and 6 just need to be done once before and after all the experiments are run, respectively.

# Starting and Stopping the PostgreSQL Service
You can start the PostgreSQL service using `start-database.sh`:
```
./setup/postgresql/start-database.sh
```

To stop the PostgreSQL service after running experiments, we can use `stop-database.sh`:
```
./setup/postgresql/stop-database.sh
```

# Creating the Crossfilter user
The experiments use a specific PostgreSQL user called "ssbuser" to manage the database tables. If this user does not yet exist, you can create this user, using the `create-user.sh` script:
```
./setup/postgresql/create-user.sh
```

# Loading Datasets
There is one script to load data of any scale factor: `load-ssb-data.sh`. Scale factor is specified in the `ssb.config.json` file in the root director. However, the scripts assume you have already generated the data of the appropriate scale factor (using the `generate_data.sh` script). You can run this script directly as follows:
```
./setup/postgresql/load-ssb-data.sh
```
