#!/bin/bash

for docx_file in data/*.docx
do
  python3 pbv.py $docx_file
done
