#!/bin/bash

#data/flights/workflows

if [ "$#" -ne 5 ]; then
  echo "You must enter exactly 5 command line arguments"
  echo "Usage: ./run-workflows-for-dataset.sh [env folder location] [scale factor] [driver] [run folder name] [total runs]"
  echo "Example: ./run-workflows-for-dataset.sh ../env 1 monetdb results/run_1 1"
  exit 0
fi

#set -x

# the virtual environment to use
ENVIR_FOLDER=$1
#dataset size/scale factor
SCALE_FACTOR=$2
# which database driver to test
DRIVER=$3
# to keep track of which run it was
RUN_FOLDERNAME=$4
# total runs
TOTAL_RUNS=$5

if [ -f "stop_scripts" ]; then
  echo "stopping execution run-workflows-for-dataset.sh"
  exit 0
fi

RUN_ID=0
while [ $RUN_ID -ne $TOTAL_RUNS ]
do
  # to store results for this specific case
  RESULT_DESTINATION="${RUN_FOLDERNAME}/sf_${SCALE_FACTOR}/run_${RUN_ID}/${DRIVER}"
  # make the result destination
  echo "preparing result destination folders: ${RESULT_DESTINATION}"
  mkdir -p ${RESULT_DESTINATION}

  echo "./run-workflow.sh ${ENVIR_FOLDER} ${DRIVER} ${RESULT_DESTINATION}"
  ./run-workflow.sh ${ENVIR_FOLDER} ${DRIVER} ${RESULT_DESTINATION}

  ((RUN_ID++))

  if [ -f "stop_scripts" ]; then
    echo "stopping execution run-workflows-for-dataset.sh"
    exit 0
  fi
done

