- Cài python ( dùng được cho cả MacOS và Window)
- Version: Bản mới nhất (hiện đang sử dụng Python 3.9.13 để code)
- Cài đủ thư viện cho python:
    langid: pip install langid, pip install langdetect
    doc2txt: pip install docx2txt
- Đặt các file đầu vào vào thư mục data. File đầu vào có định dạng docx với cấu trúc sau:
  + Nếu là 2 file song ngữ: <filename>(EN).docx và <filename>(VN).docx
  + Nếu là file bilingual: <tên file>(EN-VN)
- Chạy bằng câu lệnh: sh file_name.sh 
- Folder output sẽ chứa các file đầu ra. Định dạng file đầu ra: out_en_filename.txt (ví dụ với file ifrs.docx đầu vào thì 2 file xuất ra là out_en_ifrs.txt và out_vi_ifrs.docx)
        
