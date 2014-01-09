#!/bin/bash

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT_ABS_PATH=$(readlink -f $0)
# Absolute path to the directory this script is in. /home/user/bin
SCRIPT_ABS_DIR=$(dirname $SCRIPT_ABS_PATH)
BENCHMARK_SYS_DIR=$(dirname $SCRIPT_ABS_DIR)

(cd ${BENCHMARK_SYS_DIR} ; ./bin/benchSubmit.py; )

