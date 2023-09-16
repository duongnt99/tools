from ast import Import
from json.tool import main
from os import remove
from pickle import TRUE
from typing import final
import docx2txt
import re
import langid
import string
import sys

from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0 # Để kết quả xác định ngôn ngữ là nhất quán
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
    # Xử lý tiếng việt

    docx_file_path_en = sys.argv[1] # en_file = "<filename> (EN).docx"

    # Lấy tên của file docx tiếng Việt
    docx_file_path_vi = sys.argv[2] # vn_file = "<filename> (VN).docx"


    text = convert_docx_to_txt(docx_file_path_vi)

    namefile_vi = docx_file_path_vi.split("/")[1].split(".")[0]

    text_arr_vn = text.split("\n")
    
    main_text_vn = []


    for i in range(0 , len(text_arr_vn)): #created and standardized file txt
      if len(text_arr_vn[i])>3:
        text_arr_vn[i] = text_arr_vn[i].strip()
        main_text_vn.append(text_arr_vn[i])
    
    for elem in main_text_vn:
        if "VỮNG VÀNG TRONG THỬ THÁCH" in elem:
            main_text_vn.remove(elem)
    
    # print(main_text_vn[6])

    # for i in range(0 , len(main_text_vn)): #chuẩn hóa mảng
    #     if checkStringStartNumber(main_text_vn[i]) or checkStringBullet(main_text_vn[i]): # kiểm tra xem có bắt đầu là đề mục không
    #         main_text_vn[i] = main_text_vn[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục
    
    with open("./output/out_vi_"+namefile_vi+".txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(main_text_vn) + "."
        file_txt.write(string_text) 


    # Xử lý tiếng anh
    
    text = convert_docx_to_txt(docx_file_path_en)

    namefile_en = docx_file_path_en.split("/")[1].split(".")[0]

    text_arr = text.split("\n")
    main_text_arr = []


    for i in range(0 , len(text_arr)): #created and standardized file txt
        if len(text_arr[i])>3:
            text_arr[i] = text_arr[i].strip()
            main_text_arr.append(text_arr[i])

    for elem in main_text_arr:
        if "STAND FIRM IN CHALLENGES" in elem:
            main_text_arr.remove(elem)
          
    # for i in range(0 , len(main_text_arr)): #chuẩn hóa mảng
    #     if checkStringStartNumber(main_text_arr[i]) or checkStringBullet(main_text_arr[i]): # kiểm tra xem có bắt đầu là đề mục không
    #         main_text_arr[i] = main_text_arr[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục
            
    with open("./output/out_en_"+namefile_en+".txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(main_text_arr) + "."
        file_txt.write(string_text)
    
    
    
    
    print("Generate file from "+namefile_en+".docx and "+namefile_vi+".docx"+" success")
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

