#!/bin/bash

# Định nghĩa các biến
dir="./data"
woori_en=woori_en.docx
woori_vi=woori_vi.docx

# Duyệt qua tất cả các file trong thư mục
for file in $dir/*.docx; do

  # Lấy tên file
  filename=$(basename "$file")

  # Chạy woori .py với 2 tham số đầu vào là file woori_en.docx và woori_vi.docx
  python woori.py $file $woori_vi $woori_en
done