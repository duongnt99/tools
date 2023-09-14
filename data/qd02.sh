#!/bin/bash

# Định nghĩa các biến
dir="../data"
qd02_en=qd02_en.docx
qd02_vi=qd02_vi.docx

# Duyệt qua tất cả các file trong thư mục
for file in $dir/*.docx; do

  # Lấy tên file
  filename=$(basename "$file")

  # Chạy woori .py với 2 tham số đầu vào là file woori_en.docx và woori_vi.docx
  python3 qd02.py $file $qd02_vi $qd02_en
done