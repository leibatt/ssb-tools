#!/bin/bash

# start postgresql
current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

${current_dir}/../postgresql/./start-database.sh
