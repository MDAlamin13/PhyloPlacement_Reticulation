#!/bin/bash
taxa=$1
for((rep=1;rep<=10;rep++))
do
./run_job.sh $rep $taxa
done 
