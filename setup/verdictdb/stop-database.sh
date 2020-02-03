#!/bin/bash

# stop postgresql
current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

${current_dir}/../postgresql/./stop-database.sh
