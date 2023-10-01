#!/bin/bash

for docx_file in data/*.docx
do
  python bilingual.py "$docx_file"
done
