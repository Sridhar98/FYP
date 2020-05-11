#!/bin/bash

for i in {30..52}
do
	string="image_"
	string+=${i}
	string+=".jpg"
	python combiningFormat.py --path ${string}
	python ensembleMethod.py --path ${string}
done
