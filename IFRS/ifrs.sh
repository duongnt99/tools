#!/bin/bash

for docx_file in data/*.docx
do
  python3 ifrs.py $docx_file
done
