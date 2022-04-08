#!/bin/bash

hdfs dfs -rm orders/input/order_bd.csv
hdfs dfs -mkdir orders
hdfs dfs -mkdir orders/input

hdfs dfs -put order_bd.csv orders/input
