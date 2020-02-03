#!/bin/bash

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"

verdictdb_config="${root_dir}/verdictdb.config.json"
ssb_config="${root_dir}/ssb.config.json"

echo "python ${current_dir}/dropScrambles.py ${verdictdb_config} ${ssb_config}"
python ${current_dir}/dropScrambles.py ${verdictdb_config} ${ssb_config}
