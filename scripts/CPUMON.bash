#!/bin/bash

MONPID=$1
INTERVAL=${2-'60'}

psoptions="--no-heading -opcpu -orss -ovsize"

#Single loop unroll to create a do/while loop. (And skip the sleep on the first run)
ps ${psoptions} -p ${MONPID}

while [ $(( 1 - $? )) ]
do
        sleep $INTERVAL
        ps ${psoptions} -p ${MONPID}
done
