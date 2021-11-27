#!/bin/bash
echo 'Running Bot $1 time(s)'   
i=0
while [ $i -le $1 ]
do
  python3 client.py #>> scores.txt
  sleep 1 
  ((i++))
done
do python3 media.py