# HD-MapReduce
Hadoop MapReduce Algorithm for Python 3 

## Exercise
We have a need to solve the problem of forming a list of recommended products for an online store user using a cross-correlation algorithm (having many tuples of objects, for each possible pair of objects, count the number of tuples where they meet together).

1. **Implement two algorithms on MapReduce**:
    - Cross Correlation Pairs
    - Cross Correlation Stripes
 
2. **Implement order database generator** (or take a ready-made one). 

    _Take into account that the order consists of an arbitrary number of items (goods)._

3. **Process the order database with a cross-correlation algorithm** (count the number of occurrences of each pair of products).

4. Implement the Expert Advisor component without applying the MapReduce pattern.
The product name is entered. 10 products are displayed, which are most often
bought with a given product. Reading the results of the algorithm
cross-correlations from HDFS are implemented manually.

    _(for Java — using the FileSystem API, for Python — using the pyhdfs library)_
    
## Solving methods

### Scheme

![image](https://user-images.githubusercontent.com/31628014/162428663-69753f47-2ad5-40fc-a16f-c6d8c12c702a.png)

### 1st Method — Pairs

Each mapper accepts a tuple (a list of products in the buyer's basket) as input and generates all possible pairs of objects. At the output, we initiate key-value pairs, where the key is a pair of goods, and the value is 1.

Reduce sums up all the counters of all pairs.

**+**

   + no memory costs
   + simple implementation

**-**

   - costly sorting and distribution process

### 2nd Method — Stripes

Grouping pairs together into an associative array (dictionary). Each mapper accepts a tuple (a list of products in the buyer's basket) for each object counts the number of meetings with another object (which will be as a key).

At the Reduce stage, we will perform an element-by-element summation of dictionaries.

**+**

   + fewer sorting and distribution operations

**-**

   - the memory limit for associative arrays
   - is a more complex implementation

## Solve

### Pre-installations

You need to install the library `pyhdfs`.

`pip3 install pyhdfs`

Before starting work, you need to make sure that all scripts have permission to execute, and also that hadoop is running.

### Preparation of the database of online orders

#### Generator

Source code of `generate.py`

```
import csv
import random

EXAMPLES = ['bread', 'flour', 'cheese', 'rice', 'cereal', 'porridge', 'steak',
            'beef', 'onion', 'sausage', 'egg', 'fish', 'spaghetti', 'beer',
            'burger', 'chicken', 'orange', 'apple', 'pear', 'cucumber']

items = [sorted(random.sample(EXAMPLES, random.randint(2, 5))) for _ in range(1000)]
items.sort()
with open('order_bd.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for item in items:
        writer.writerow(item)
```

#### Upload to HDFS

Source code of `copyInput.sh`

```
#!/bin/bash

hdfs dfs -rm orders/input/order_bd.csv
hdfs dfs -mkdir orders
hdfs dfs -mkdir orders/input

hdfs dfs -put order_bd.csv orders/input
```

### Pairs algorithm

#### Map

Source code of `pairs_map.py`

```
import sys

for line in sys.stdin:
    collection = line.lower().strip('\r\n ').split(",")
    for index_1 in range(len(collection)):
        for index_2 in range(index_1 + 1, len(collection)):
            if collection[index_1] > collection[index_1]:
                print(f'{collection[index_1]}--{collection[index_2]}\t1')
            else:
                print(f'{collection[index_2]}{collection[index_1]}\t1')
```

_Here, repeated consideration of pairs is excluded. This optimizes the algorithm._

#### Reduce

Source code of `pairs_reduce.py`

```
import sys

(lastKey, sum) = (None, 0)

for line in sys.stdin:
    (key, value) = line.replace('\r\n ', '').split("--")

    if lastKey and lastKey != key:
        print(lastKey + '\t' + str(sum))
        (lastKey, sum) = (key, int(value))
    else:
        (lastKey, sum) = (key, sum + int(value))
```

#### Run

Source code of `runPairs.sh`

```
#!/bin/bash

hdfs dfs -rm -r orders/output

yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-D mapreduce.job.name="HD-MapReduce" \
-files `pwd`/pairs_map.py,`pwd`/pairs_reduce.py \
-input orders/input/ \
-output orders/output/ \
-mapper `pwd`/pairs_map.py \
-reducer `pwd`/pairs_reduce.py
```

### Stripe algorithm

#### Map

Source code of `stripe_map.py`

```
import sys

for line in sys.stdin:
    collection = line.lower().strip('\r\n ').split(",")
    for item in collection:    
        H = {}
        for item2 in collection:        
            if item2 in H:
                H[item2] += 1
            else:
                H[item2] = 1
        print("{}--{}".format(item, H))
```

_Here, repeated consideration of pairs is excluded. This optimizes the algorithm._

#### Reduce

Source code of `stripe_reduce.py`

```
import sys

(lastKey, s) = (None, "{}")

s = eval(s)
for line in sys.stdin:
    (key, value) = line.replace('\r\n ', '').split("--")
    value = eval(value)
    if lastKey and lastKey != key:
        print(f'{lastKey}:', end='')
        for i, j in s.items():
            if i == lastKey:
                continue 
            print(f'{i}={j}', end=';')
        print()
        (lastKey, s) = (key, value)
    else:
        for i in value:
            s[i] = s[i] + value[i] if i in s else value[i]
        lastKey = key
```

#### Run

Source code of `runPairs.sh`

```
#!/bin/bash

hdfs dfs -rm -r orders/output

yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-D mapreduce.job.name="HD-MapReduce" \
-files `pwd`/stripe_map.py,`pwd`/stripe_reduce.py \
-input orders/input/ \
-output orders/output/ \
-mapper `pwd`/stripe_map.py \
-reducer `pwd`/stripe_reduce.py
```

### Implement the Expert Advisor

#### For Pairs algorithm

```
import pyhdfs

fs = pyhdfs.HdfsClient("localhost:9870", user_name="yan")
print("Connected")
fs.copy_to_local("/user/yan/orders/output/part-00000", "info")
inf = {}
with open("info", "r") as f:
    for line in f.read().split("\n"):
        if line:
            key, value = line.split(":")
            value = value.split("\t")
            if key in inf:
                inf[key].append(value)
            else:
                inf[key] = [value, ]
print(inf)
choice = input("Enter a meal:")
if choice in inf:
    items = sorted(inf[choice], key=lambda x: x[1], reverse=True)[:10]
    for item in items:
        print("{}, {} times".format(*item))
```

#### For Stripe algorithm

```
import pyhdfs

fs = pyhdfs.HdfsClient("localhost:50070", user_name="yan")
print("Connected")
fs.copy_to_local("/user/yan/orders/output/part-00000", "info")
inf = {}
with open("info", "r") as f:
    inf = {}
    for line in f.read().split("\n"):
        line = line.split(':')
        if line == ['']:
            continue
        inf[line[0]] = {i.split('=')[0]: i.split('=')[1] for i in line[1].split(';')[:-1]}
choice = input("Enter a meal:")
if choice in inf:
    items = sorted_x = sorted(inf[choice].items(), key=lambda kv: kv[1], reverse=True)
    for item in items:
        print("{}, {} times".format(*item))
```
