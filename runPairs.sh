#!/bin/bash

hdfs dfs -rm -r orders/output


yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-D mapreduce.job.name="Lab 2 of MapReduce" \
-files `pwd`/pairs_map.py,`pwd`/pairs_reduce.py \
-input orders/input/ \
-output orders/output/ \
-mapper `pwd`/pairs_map.py \
-reducer `pwd`/pairs_reduce.py
