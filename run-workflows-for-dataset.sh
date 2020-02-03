#!/bin/bash

#data/flights/workflows

if [ "$#" -ne 4 ]; then
  echo "You must enter exactly 5 command line arguments"
  echo "Usage: ./run-workflows-for-dataset.sh [env folder location] [scale factor] [driver] [run folder name]"
  echo "Example: ./run-workflows-for-dataset.sh ../env 1 monetdb results/run_1"
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

# to store results for this specific case
RESULT_DESTINATION="${RUN_FOLDERNAME}/sf_${SCALE_FACTOR}/${DRIVER}"

# make the result destination
echo "preparing result destination folders: ${RESULT_DESTINATION}"
mkdir -p ${RESULT_DESTINATION}

if [ -f "stop_scripts" ]; then
  echo "stopping execution run-workflows-for-dataset.sh"
  exit 0
fi

echo "./run-workflow.sh ${ENVIR_FOLDER} ${DRIVER} ${RESULT_DESTINATION}"
./run-workflow.sh ${ENVIR_FOLDER} ${DRIVER} ${RESULT_DESTINATION}

