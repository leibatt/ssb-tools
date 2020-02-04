#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "You must specify python virtual environment directory and total runs per driver"
  echo "Usage: ./run-all-workflows-all-drivers.sh [env folder location] [total runs]"
  echo "Example: ./run-all-workflows-all-drivers.sh ../env 1"
  exit 0
fi

# the virtual environment to use
ENVIR_FOLDER=$1
# total runs
TOTAL_RUNS=$2

#nicely formatted timestamp
RUN_TIMESTAMP=$(date +%m-%d-%y_%T)
RUN_FOLDERNAME="results/run_${RUN_TIMESTAMP}"

echo "removing any stop_scripts file just in case"
rm stop_scripts

echo "creating run folder ${RUN_FOLDERNAME}"
mkdir -p $RUN_FOLDERNAME

for SCALE_FACTOR in 1 2 4 8
do
  LOGFILE="${RUN_FOLDERNAME}/output.txt"
  echo "logfile for storing all output: ${LOGFILE}"

  # put updated scale factor in SSB config file
  ssb_config="ssb.config.json"
  echo "python -c \"import sys, json; config=json.load(open('${ssb_config}')); config['scale-factor'] = ${SCALE_FACTOR}; json.dump(config,open('ssb.config.json','w')); \"" >> $LOGFILE 2>&1
  python -c "import sys, json; config=json.load(open('${ssb_config}')); config['scale-factor'] = ${SCALE_FACTOR}; json.dump(config,open('ssb.config.json','w'))"
  data_folder=`python -c "import sys, json; print(json.load(open('${ssb_config}'))['data-folder'])"`
  workflow_file=`python -c "import sys, json; print(json.load(open('${ssb_config}'))['workflow-file'])"`


  echo "stopping all DBMSs" >> $LOGFILE 2>&1
  setup/./stop-all.sh >> $LOGFILE 2>&1
  echo "starting all DBMSs" >> $LOGFILE 2>&1
  setup/./start-all.sh >> $LOGFILE 2>&1

  echo "activating environment" >> $LOGFILE 2>&1
  source ${ENVIR_FOLDER}/bin/activate >> $LOGFILE 2>&1

  if [ -f "stop_scripts" ]; then
    echo "stopping execution of run-all-workflows-all-drivers.sh" >> $LOGFILE 2>&1
    deactivate
    exit 0
  fi

  if [ ! -d "${data_folder}/sf_${SCALE_FACTOR}" ]; then
    echo "Cannot find folder ${data_folder}/sf_${SCALE_FACTOR}. generating SSB data for scale factor ${SCALE_FACTOR}" >> $LOGFILE 2>&1
    ./generate_data.sh >> $LOGFILE 2>&1
  else
    echo "data appears to be generated for scale factor ${SCALE_FACTOR} already. Moving on..." >> $LOGFILE 2>&1
  fi

  echo "loading datasets for scale factor ${SCALE_FACTOR} into all DBMSs" >> $LOGFILE 2>&1
  ./setup/load-ssb-data.sh >> $LOGFILE 2>&1

  if [ -f "stop_scripts" ]; then
    echo "stopping execution of run-all-workflows-all-drivers.sh" >> $LOGFILE 2>&1
    deactivate
    exit 0
  fi

  echo "generating SSB queries for dataset using monetdb" >> $LOGFILE 2>&1
  python query_randomizer.py --driver-name monetdb >> $LOGFILE 2>&1

  echo "mkdir -p ${RUN_FOLDERNAME}/sf_${SCALE_FACTOR}" >> $LOGFILE 2>&1
  mkdir -p ${RUN_FOLDERNAME}/sf_${SCALE_FACTOR}
  echo "cp ${workflow_file}.generated ${RUN_FOLDERNAME}/sf_${SCALE_FACTOR}/ssb_workflow.json" >> $LOGFILE 2>&1
  cp ${workflow_file}.generated ${RUN_FOLDERNAME}/sf_${SCALE_FACTOR}/ssb_workflow.json

  echo "deactivating environment" >> $LOGFILE 2>&1
  deactivate >> $LOGFILE 2>&1

  for SCRAMBLE_PERCENT in 10
  do
    DRIVER="verdictdb"
    echo "running SSB with ${DRIVER} and scale factor ${SCALE_FACTOR}" >> $LOGFILE 2>&1
    echo "eventually saving to ${RUN_FOLDERNAME}/sf_${SCALE_FACTOR}/${DRIVER}-${SCRAMBLE_PERCENT}" >> $LOGFILE 2>&1
    echo "python -c \"import sys, json; config=json.load(open('verdictdb.config.json')); config['scramblePercent'] = ${SCRAMBLE_PERCENT}; json.dump(config,open('verdictdb.config.json','w')); \"" >> $LOGFILE 2>&1
    python -c "import sys, json; config=json.load(open('verdictdb.config.json')); config['scramblePercent'] = ${SCRAMBLE_PERCENT}; json.dump(config,open('verdictdb.config.json','w'))"
    echo "./run-workflows-for-dataset.sh $ENVIR_FOLDER $SCALE_FACTOR $DRIVER $RUN_FOLDERNAME $TOTAL_RUNS >> $LOGFILE" 2>&1
    ./run-workflows-for-dataset.sh $ENVIR_FOLDER $SCALE_FACTOR $DRIVER $RUN_FOLDERNAME $TOTAL_RUNS >> $LOGFILE 2>&1
  
    if [ -f "stop_scripts" ]; then
      echo "stopping execution of run-all-workflows-all-drivers.sh" >> $LOGFILE 2>&1
      exit 0
    fi

    # move the verdictdb folders to the right place
    RUN_ID=0
    while [ $RUN_ID -ne $TOTAL_RUNS ]
do
      echo "mv ${RUN_FOLDERNAME}/sf_${SCALE_FACTOR}/run_${RUN_ID}/${DRIVER} ${RUN_FOLDERNAME}/sf_${SCALE_FACTOR}/run_${RUN_ID}/${DRIVER}-${SCRAMBLE_PERCENT}" >> $LOGFILE 2>&1
      mv ${RUN_FOLDERNAME}/sf_${SCALE_FACTOR}/${DRIVER} ${RUN_FOLDERNAME}/sf_${SCALE_FACTOR}/${DRIVER}-${SCRAMBLE_PERCENT} >> $LOGFILE 2>&1
    done
  done

  for DRIVER in "monetdb" "postgresql" "sqlite" "duckdb"
  #for DRIVER in "monetdb" "postgresql"
  do
    echo "running SSB with ${DRIVER} and scale factor ${SCALE_FACTOR}" >> $LOGFILE 2>&1
    echo "./run-workflows-for-dataset.sh $ENVIR_FOLDER $SCALE_FACTOR $DRIVER $RUN_FOLDERNAME $TOTAL_RUNS >> $LOGFILE" 2>&1
    ./run-workflows-for-dataset.sh $ENVIR_FOLDER $SCALE_FACTOR $DRIVER $RUN_FOLDERNAME $TOTAL_RUNS >> $LOGFILE 2>&1

    if [ -f "stop_scripts" ]; then
      echo "stopping execution of run-all-workflows-all-drivers.sh" >> $LOGFILE 2>&1
      exit 0
    fi
  done
done

