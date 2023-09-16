#!/bin/bash

# Loop through all the docx files in the data directory
for file in data/*.docx; do
  # Get the base name of the file without the extension
  base=${file%.docx}
  # Check if the file has EN suffix
  if [[ $base == *"(EN)" ]]; then
    # Remove the EN suffix and add VN suffix to get the corresponding VN file name
    vn_file=${base/"(EN)"/"(VN)"}.docx
    # Check if the VN file exists
    if [ -f $vn_file ]; then
      # Use the pair of files as input for the python file
      python qd02.py $file $vn_file
    fi
  fi
done
