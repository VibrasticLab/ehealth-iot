#!/bin/bash

while true;do

export RNDNUM=$(echo $[ $RANDOM % 40 + 10 ])

for i in {1..10};do
    export RNDNUM="$(echo $[ $RANDOM % 40 + 10 ]) $RNDNUM"
done

echo $RNDNUM

sleep 1

done
