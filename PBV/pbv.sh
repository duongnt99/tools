#!/bin/bash

for docx_file in data/*.docx
do
  python pbv.py $docx_file
done
