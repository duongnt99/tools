#!/bin/bash

for docx_file in data/*.docx
do
  python3 bilingual.py "$docx_file"
done
