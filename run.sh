#!/bin/bash
echo 'Running Bot $1 time(s)'   
i=0
while [ $i -lt $1 ]
do
  python3 student.py #>> scores.txt
  sleep 1 
  ((i++))
done
#python3 media.py