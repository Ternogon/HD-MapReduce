#!/bin/bash

hdfs dfs -rm -r orders/output


yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-D mapreduce.job.name="Lab 2 of MapReduce" \
-files `pwd`/stripe_map.py,`pwd`/stripe_reduce.py \
-input orders/input/ \
-output orders/output/ \
-mapper `pwd`/stripe_map.py \
-reducer `pwd`/stripe_reduce.py
