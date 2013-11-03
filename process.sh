#!/bin/bash

cat dl/*.csv | sort | uniq | grep ",[a-zA-Z ]\+ [0-9]\+ - [a-zA-Z ]\+ [0-9]\+," | awk -F, '{ OFS=","; print $1, $4; }' | sed -e "s/\([0-9]\{2\}\)\/\([0-9]\{2\}\)\/\([0-9]\{4\}\)/\3\1\2/" | sort | grep -v "201.09" > games-ordered.csv
