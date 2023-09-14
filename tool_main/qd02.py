from ast import Import
from os import remove
from pickle import TRUE
import docx2txt
import re
import langid
import string


from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0 # Để kết quả xác định ngôn ngữ là nhất quán, hàm này trả về 3 kết quả: vietnamese, english, unknown. Hầu như unknow đều là tiếng anh, trừ một số trường hợp đặc biệt
def check_language(string):
    lang = detect(string) # Trả về mã ngôn ngữ theo chuẩn ISO 639-1
    if lang == "en":
        return "English"
    elif lang == "vi":
        return "Vietnamese"
    else:
        return "Unknown"

def convert_docx_to_txt(docx_file_path):
  """Converts a DOCX file to a TXT file.

  Args:
    docx_file_path (str): The path to the DOCX file.

  Returns:
    str: The text content of the DOCX file.
  """

  with open(docx_file_path, 'rb') as docx_file:
    text = docx2txt.process(docx_file)

  return text

def checkStringBullet(string): # kiểm tra đầu mục có bắt đầu bằng a), b), c), d)
    if string.startswith(("a)","b)","c)","d)")):
        return True
    else:
        return False

def checkStringStartNumber(string): # kiểm tra đầu mục có bắt đầu bằng số
    if string.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "□")):
        return True
    else:
        return False

if __name__ == '__main__':
  # Xử lý tiếng việt
    
    docx_file_path_vi, docx_file_path_en = input("Input file name QD_02 Vietnamese and English: ").split() #'qd02_vi.docx'
    text = convert_docx_to_txt(docx_file_path_vi)

    text_arr_vn = text.split("\n")
    
    main_text_vn = []

    for elem in text_arr_vn:
      if elem.startswith("--"):
        text_arr_vn.remove(elem)

    for i in range(0 , len(text_arr_vn)): #tạo và chuẩn hóa file txt, cắt dòng thừa, lấy dòng số kí tự >1
      if len(text_arr_vn[i])>1:
        text_arr_vn[i] = text_arr_vn[i].strip()
        main_text_vn.append(text_arr_vn[i])

    count_li_vn = 0 # đếm số dòng nơi nhận trong file tiếng việt, file tiếng anh không có mục này nên phải để trống
    for elem in main_text_vn:
      if elem.startswith("-"):
        count_li_vn = count_li_vn+1
    
    for i in range(0 , len(main_text_vn)): #chuẩn hóa mảng
        if checkStringStartNumber(main_text_vn[i]) or checkStringBullet(main_text_vn[i]): # kiểm tra xem có bắt đầu là đề mục không
            main_text_vn[i] = main_text_vn[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục

    with open("out_vn.txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(main_text_vn) + "."
        file_txt.write(string_text) 


    # Xử lý tiếng anh
    # docx_file_path_en = input("Input file name QĐ English(docx): ")  #'qd02_en.docx'
    text = convert_docx_to_txt(docx_file_path_en)

    text_arr = text.split("\n")
    main_text_arr = []

    for i in range(0 , len(text_arr)): #tạo và chuẩn hóa file txt, cắt dòng thừa, lấy dòng số kí tự >1
        if len(text_arr[i])>1:
            text_arr[i] = text_arr[i].strip()
            main_text_arr.append(text_arr[i])
    
    index = -1 # Giá trị mặc định nếu không tìm thấy
    for i in range(len(main_text_arr)):
      if main_text_arr[i].startswith("PRIME MINISTER"):
        index = i # Lưu lại chỉ số của phần tử
        break # Thoát khỏi vòng lặp

    # Cắt mảng từ chỉ số tìm được trở đi
    if index != -1: # Nếu tìm thấy phần tử
      main_text = main_text_arr[index:] # Cắt mảng
    else: # Nếu không tìm thấy phần tử
      main_text = [] # Trả về mảng rỗng

    for elem in main_text:
      if ("Allens" in elem):
        main_text.remove(elem)

    for i in range(1, len(main_text)):
      if(main_text[i]=="ISSUING"):
        main_text[i] = main_text[i]+" "+main_text[i+1]+" "+main_text[i+2]

    # Gép câu issue
    merge_issue_arr = []
    for elem in main_text:
      if elem.startswith("ISSUING"):
        # Thêm phần tử vào mảng mới
        merge_issue_arr.append(elem)
        # Bỏ qua hai phần tử kế tiếp trong mảng ban đầu
        main_text.remove(main_text[main_text.index(elem) + 1])
        main_text.remove(main_text[main_text.index(elem) + 1])
      # Các trường hợp khác
      else:
        # Thêm phần tử vào mảng mới
        merge_issue_arr.append(elem)

    sub1 = "PRIME MINISTER OF THE GOVERNMENT"
    sub2 = "SOCIALIST REPUBLIC OF VIETNAM"
    standardized_arr = []
    standardized_arr.append(sub1)
    standardized_arr.append(sub2)
    for i in range (1, len(merge_issue_arr)-1):
      standardized_arr.append(merge_issue_arr[i])
    
    index_li_vn = standardized_arr.index("On behalf of the Prime Minister")# Chèn số dòng trống nơi gửi văn bản
    for i in range(count_li_vn+1):
      standardized_arr.insert(index_li_vn, "")

    index_notice_bonus_vn = standardized_arr.index("CHAPTER 1") # Trống dòng (Ban hành kèm theo Quyết định số 02/2013/QĐ-TTg ngày 14 tháng 01 năm 2013 của Thủ tướng Chính phủ)
    standardized_arr.insert(index_notice_bonus_vn,"")

    for i in range(0 , len(standardized_arr)): #chuẩn hóa mảng
        if checkStringStartNumber(standardized_arr[i]) or checkStringBullet(standardized_arr[i]): # kiểm tra xem có bắt đầu là đề mục không
            standardized_arr[i] = standardized_arr[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục

    with open("out_en.txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(standardized_arr) + "."
        file_txt.write(string_text) 

    print("Done!")
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

