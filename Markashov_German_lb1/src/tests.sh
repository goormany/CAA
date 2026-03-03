#!/bin/bash

g++ main.cpp -o main

for i in {2..20}; do
	echo "N = $i"
	echo "$i" | ./main
	echo -e "\n"
done
