# using run-workflow.sh with VerdictDB
To run SSB using the main bash script and VerdictDB (*after* the PostgreSQL experiments have been run already), run the following in the root repository folder (i.e., the `ssb-test` root folder):
```
./run-workflow.sh [env folder location] verdictdb [result destination]
```

Example:
```
./run-workflow.sh ../env verdictdb results/test
```

NOTE: VerdictDB alters the PostgreSQL setup, so you should *only run PostgreSQL experiments after removing all VerdictDB scrambles!!!!*

NOTE: this script assumes that postgresql is setup already. You can easily setup postgresql using the postgresql scripts or the verdicdb scripts (which point to the postgresql scripts anyway).

NOTE: this script assumes you are using a virtual environment to run Python with SSB. "env folder location" refers to the location of the Python virtual environment setup for running SSB.

NOTE: this assumes someone already went through the trouble of setting up PostgreSQL separately (these scripts will not install and setup postgresql for you! only the ssb-test database)

NOTE: this does not finally stop the database! this step should be handled either manually or using a larger script that processes multiple workflows...

# Using the VerdictDB scripts
There is a bash script saved in this folder (`setup/verdictdb`) for basic things that need to be done with Postgresql for VerdictDB (these point to the PostgreSQL scripts in `setup/postgresql`). To run any of these scripts, simply run them directly in the root folder of the ssb-test repository:
```
./setup/verdictdb/[scriptname].sh
```

For example, to start the ssb-test database:
```
./setup/verdictdb/start-database.sh
```

To run the experiments with SSB and VerdictDB, you will need the PostgreSQL Python connector: `psycopg2`, and the VerdictDB connector `pyverdict`.

An example of how to run experiments using VerdictDB with the benchmark (using the root repository folder):
```
python run_benchmark_queries.py --driver-name verdictdb
```

# Experiment flow
In general, all of the following steps should be carried out to have a clean run with VerdictDB. The following sections explains each of the scripts.
1. start the database (using `start-database.sh`)
2. load the data (e.g., `load-ssb-data.sh`)
3. for each separate run of SSB:
    1. stop the database (using `stop-database.sh`)
    2. start the database (using `start-database.sh`)
    3. run SSB
4. stop the database one final time (using `stop-database.sh`)

Note that steps 1, 2 and 4 just need to be done once before and after all the experiments are run, respectively.

# Starting and Stopping the PostgreSQL Service for VerdictDB
You can start the PostgreSQL service for VerdictDB using `start-database.sh`:
```
./setup/verdictdb/start-database.sh
```

To stop the PostgreSQL service after running experiments, we can use `stop-database.sh`:
```
./setup/verdictdb/stop-database.sh
```

# Creating the SSB user
The experiments use a specific PostgreSQL user called "ssbuser" to manage the database tables. Since VerdictDB depends on PostgreSQL, then we also need this user to run experiments with VerdictDB. If this user does not yet exist, you can create this user, using the `create-user.sh` script:
```
./setup/verdictdb/create-user.sh
```

# Loading Datasets

There is one script to load data of any scale factor: `load-ssb-data.sh`. Scale factor is specified in the `ssb.config.json` file in the root director. However, the scripts assume you have already generated the data of the appropriate scale factor (using the `generate_data.sh` script). You can run this script directly as follows:
```
./setup/verdictdb/load-ssb-data.sh
```
Note that loading the data is not necessary if you have already done it for PostgreSQL.

# creating and dropping VerdictDB scrambles
VerdictDB works by creating and using "scrambles" to execute queries. These scrambles need to be setup *before* experiments are run for VerdictDB. To create scrambles, run the following script with a Python environment that contains `psycopg2` and `pyverdict`:
```
python setup/verdictdb/createScrambles.py [verdictdb config] [ssb config]
```

You can easily remove all scrambles using this Python script:
```
python setup/verdictdb/dropScrambles.py [verdictdb config] [ssb config]
```

There are dedicated scripts to do the above in the setup folder:
```
./setup/verdictdb/create_scrambles.sh
./setup/verdictdb/drop_scrambles.sh
```
