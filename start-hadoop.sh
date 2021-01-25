#!/bin/sh

wget https://covid.ourworldindata.org/data/owid-covid-data.csv
cat owid-covid-data.csv | tail -n +2 > file

hadoop fs -mkdir -p /user/hdoop/input/
hadoop fs -put input/file /user/hdoop/input/

hadoop jar /home/hdoop/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
-mapper /home/hdoop/mapper.py \
-reducer /home/hdoop/reducer.py \
-input /user/hdoop/input/file \
-output /user/hdoop/output
