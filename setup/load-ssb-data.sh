#!/bin/bash

root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"

SOURCE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
for DBMS in $( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && ls -d */ )
do
  if [ -f "${root_dir}/stop_scripts" ]; then
    echo "stopping execution of ${root_dir}/setup/load-ssb-data.sh" >> $LOGFILE 2>&1
    deactivate
    exit 0
  fi
  
  if [ "$DBMS" != "verdictdb/" ]; then # verdictdb just uses postgresql
    echo "${SOURCE}/${DBMS}./load-ssb-data.sh"
    ${SOURCE}/${DBMS}./load-ssb-data.sh
  else
    # setup the scrambles
    echo "${SOURCE}/${DBMS}./create_scrambles.sh"
    ${SOURCE}/${DBMS}./create_scrambles.sh
  fi
done
