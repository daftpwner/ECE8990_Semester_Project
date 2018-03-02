#!/bin/bash

# Create the directory (needed since dfs cleared on reboot)
/usr/local/hadoop/bin/hdfs dfs -mkdir -p $(pwd)

# Delete current dfs input/midput/output folders
/usr/local/hadoop/bin/hdfs dfs -rm -r $(pwd)

# Create the directory (needed since dfs cleared on reboot)
/usr/local/hadoop/bin/hdfs dfs -mkdir -p $(pwd)

# Copy input folder to dfs
/usr/local/hadoop/bin/hdfs dfs -put input/data/labeled_data.csv $(pwd)/input

# Launch first job
/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.5.jar \
-input  $(pwd)/input \
-output $(pwd)/output \
-mapper "/bin/cat" \
-reducer "/bin/cat"

# Delete midput/output folders
rm -r $(pwd)/output

# Copy down midput/output folders
/usr/local/hadoop/bin/hdfs dfs -get $(pwd)/output
