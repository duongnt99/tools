#!/bin/bash

# Định nghĩa các biến
dir="/home/user/data"
nd01_en=nd01_en.docx
nd01_vi=nd01_vi.docx

# Duyệt qua tất cả các file trong thư mục
for file in $dir/*.docx; do

  # Lấy tên file
  filename=$(basename "$file")

  # Chạy woori .py với 2 tham số đầu vào là file woori_en.docx và woori_vi.docx
  python nd01.py $file $nd01_vi $nd01_en
done