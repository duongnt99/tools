#!/bin/bash

# Định nghĩa các biến
dir="/root/snap/lxd/current/data"
cotecon_en=cotecon_en.docx
cotecon_vi=cotecon_vi.docx

# Duyệt qua tất cả các file trong thư mục
for file in $dir/*.docx; do

  # Lấy tên file
  filename=$(basename "$file")

  # Chạy woori .py với 2 tham số đầu vào là file woori_en.docx và woori_vi.docx
  python cotecon.py $file $cotecon_vi $cotecon_en
done