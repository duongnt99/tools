from ast import Import
from cmath import isnan
from json.tool import main
from os import remove
from pickle import TRUE
from typing import final
import docx2txt
import re
import langid
import string
import sys
import nltk

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

    bucket_arr_vn = []
    for i in range(0 , len(main_text_vn)):
        sentence = nltk.sent_tokenize(main_text_vn[i]) #Tách đoạn thành câu
        bucket_arr_vn.append(sentence)
 
    standardized_arr_vn = []
    for i in range (0,len(bucket_arr_vn)):
        if(len(bucket_arr_vn[i])>1): # tìm đoạn văn
            for j in range(0, len(bucket_arr_vn[i])):
                standardized_arr_vn.append(bucket_arr_vn[i][j]) # Lấy các câu trong đoạn văn
        else:
            string_text = "".join(bucket_arr_vn[i])
            standardized_arr_vn.append(string_text) #lấy các câu đơn
    
    for elem in standardized_arr_vn:
        if len(elem)<10: # xóa những dòng bị thừa
            standardized_arr_vn.remove(elem)
    

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
          
    bucket_arr_en = []
    for i in range(0 , len(main_text_arr)):
        sentence = nltk.sent_tokenize(main_text_arr[i]) #Tách đoạn thành câu
        bucket_arr_en.append(sentence)
 
    standardized_arr_en = []
    for i in range (0,len(bucket_arr_en)):
        if(len(bucket_arr_en[i])>1): # tìm đoạn văn
            for j in range(0, len(bucket_arr_en[i])): 
                standardized_arr_en.append(bucket_arr_en[i][j]) # Lấy các câu trong đoạn văn
        else:
            string_text = "".join(bucket_arr_en[i]) 
            standardized_arr_en.append(string_text) #lấy các câu đơn
    
    for elem in standardized_arr_en:
        if len(elem)<10: # Xóa những dòng bị thừa
            standardized_arr_en.remove(elem)

    with open("./output/out_en_"+namefile_en+".txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(standardized_arr_en) + "."
        file_txt.write(string_text) 
    
    with open("./output/out_vi_"+namefile_vi+".txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(standardized_arr_vn) + "."
        file_txt.write(string_text) 
    
    
    print("Generate file from "+namefile_en+".docx and "+namefile_vi+".docx"+" success")
        

