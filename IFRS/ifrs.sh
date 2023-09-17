#!/bin/bash

for docx_file in data/*.docx
do
  python ifrs.py "$docx_file"
done
