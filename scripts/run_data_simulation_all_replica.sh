#!/bin/bash
for((rep=1;rep<=10;rep++))
do
python placement_data_simulate.py ms_commands_1_20.txt 20.txt $rep 20 .00001
done
