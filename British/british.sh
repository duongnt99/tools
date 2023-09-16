#!/bin/bash

for docx_file in data/*.docx
do
  python3 british.py $docx_file
done
