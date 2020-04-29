#!/bin/sh
Working_Directory=$(pwd)
for file in $Working_Directory/inputs/*; do
        echo "$(basename "$file")"
        python recognition.py --image-path="$(basename "$file")"
        python ensembleMethod.py --image-path="$(basename "$file")"
done
