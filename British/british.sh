#!/bin/bash

for docx_file in data/*.docx
do
  python british.py "$docx_file"
done
