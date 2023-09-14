from ast import Import
from json.tool import main
from os import remove
from pickle import TRUE
from typing import final
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
    if string.startswith(("a","b","c","d","e")):
        return True
    else:
        return False

def checkStringStartNumber(string): # kiểm tra đầu mục có bắt đầu bằng số
    if string.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "□")):
        return True
    else:
        return False

if __name__ == '__main__':
    docx_file_path_vi, docx_file_path_en = input("Input file name nd_01 Vietnamese and English: ").split() #'nd01_vi.docx'
    # Xử lý tiếng việt
    # docx_file_path_vi = input("Input file name NĐ Vietnamese(docx): ") #'nd01_vi.docx'
    # docx_file_path_vi = 'nd01_vi.docx'
    text = convert_docx_to_txt("./data/"+docx_file_path_vi)

    text_arr_vn = text.split("\n")
    
    main_text_vn = []

    for elem in text_arr_vn:
      if elem.startswith("--"):
        text_arr_vn.remove(elem)

    for i in range(0 , len(text_arr_vn)): #created and standardized file txt
      if len(text_arr_vn[i])>1:
        text_arr_vn[i] = text_arr_vn[i].strip()
        main_text_vn.append(text_arr_vn[i])
    
    for i in range(0 , len(main_text_vn)): #chuẩn hóa mảng
        if checkStringStartNumber(main_text_vn[i]) or checkStringBullet(main_text_vn[i]): # kiểm tra xem có bắt đầu là đề mục không
            main_text_vn[i] = main_text_vn[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục

    with open("./output/out_vn_nd01.txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(main_text_vn) + "."
        file_txt.write(string_text) 


    # Xử lý tiếng anh
    # docx_file_path_en = input("Input file name NĐ English(docx): ")  #'nd01_en.docx'
    # docx_file_path_en = 'nd01_en.docx'
    text = convert_docx_to_txt("./data/"+docx_file_path_en)

    text_arr = text.split("\n")
    main_text_arr = []

    for i in range(0 , len(text_arr)): #created and standardized file txt
        if len(text_arr[i])>1:
            text_arr[i] = text_arr[i].strip()
            main_text_arr.append(text_arr[i])
    
    for elem in main_text_arr:
        if elem == "www.LuatVietnam.vn":
            main_text_arr.remove(elem)
        elif "Legal Forum" in elem:
            main_text_arr.remove(elem)
            
    for i in range(0, len(main_text_arr)):
        if main_text_arr[i].startswith("www.LuatVietnam.vn"):
            main_text_arr[i] = main_text_arr[i].replace("www.LuatVietnam.vn", "")
    
    final_arr = []
    final_arr.append("THE GOVERNMENT")
    final_arr.append("SOCIALIST REPUBLIC OF VIETNAM")
    final_arr.append("Independence - Freedom - Happiness")

    for i in range(1, len(main_text_arr)-1):
        final_arr.append(main_text_arr[i])

    for i in range(0 , len(final_arr)): #chuẩn hóa mảng
        if checkStringStartNumber(final_arr[i]) or checkStringBullet(final_arr[i]): # kiểm tra xem có bắt đầu là đề mục không
            final_arr[i] = final_arr[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục

    with open("./output/out_en_nd01.txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(final_arr) + "."
        file_txt.write(string_text)
    
    
    
    print("Done")
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

