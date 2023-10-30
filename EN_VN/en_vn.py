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
import zipfile

from underthesea import sent_tokenize

from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0 # Để kết quả xác định ngôn ngữ là nhất quán
def is_number_comma(s):
    # Loop through each character in the string
    for ch in s:
        # If the character is not a digit or a comma, return False
        if not ch.isdigit() and ch != ",":
            return False
    # If all characters are digits or commas, return True
    return True

def is_number_dot(s):
    # Loop through each character in the string
    for ch in s:
        # If the character is not a digit or a comma, return False
        if not ch.isdigit() and ch != ".":
            return False
    # If all characters are digits or commas, return True
    return True

def is_number_comma_percent(s):
    # Loop through each character in the string
    for ch in s:
        # If the character is not a digit or a comma, return False
        if not ch.isdigit() and ch != "," and ch!="%":
            return False
    # If all characters are digits or commas, return True
    return True

def is_number_comma_dot(s):
    # Loop through each character in the string
    for ch in s:
        # If the character is not a digit or a comma, return False
        if not ch.isdigit() and ch != "," and ch!=".":
            return False
    # If all characters are digits or commas, return True
    return True

def is_number_dot_percent(s):
    # Loop through each character in the string
    for ch in s:
        # If the character is not a digit or a comma, return False
        if not ch.isdigit() and ch != "." and ch!="%":
            return False
    # If all characters are digits or commas, return True
    return True


def check_language(string):
    lang = detect(string) # Trả về mã ngôn ngữ theo chuẩn ISO 639-1
    if lang == "en":
        return "English"
    elif lang == "vi":
        return "Vietnamese"
    else:
        return "Unknown"

def convert_docx_to_txt(docx_file_path):
   
    try:
        with open(docx_file_path, 'rb') as docx_file:
            text = docx2txt.process(docx_file)
        return text
    except zipfile.BadZipFile:
        return f"Error: {docx_file_path} is not a valid zip file."

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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def preprocess_abbreviations(text):
  # Tạo một từ điển để ánh xạ những từ viết tắt và cách viết không có dấu chấm
  abbreviations = {"a.m.": "am", "p.m.": "pm", "per cent.": "percent", " co.": "co"}
  # Duyệt qua những từ viết tắt trong từ điển
  for abbr, repl in abbreviations.items():
    # Thay thế những từ viết tắt bằng cách viết không có dấu chấm trong văn bản
    text = text.replace(abbr, repl)
  # Trả về văn bản đã được xử lý
  return text

if __name__ == '__main__':
    # Xử lý tiếng việt

    docx_file_path_en = sys.argv[1] # en_file = "<filename> (EN).docx"

    # Lấy tên của file docx tiếng Việt
    docx_file_path_vi = sys.argv[2] # vn_file = "<filename> (VN).docx"


    text = convert_docx_to_txt(docx_file_path_vi)

    namefile_vi = docx_file_path_vi.split("/")[1].split(".")[0]

    text_arr_vn = text.split("\n")
    
    main_text_vn_raw = []


    for i in range(0 , len(text_arr_vn)): #created and standardized file txt
      if len(text_arr_vn[i])>3:
        text_arr_vn[i] = text_arr_vn[i].strip()
        main_text_vn_raw.append(text_arr_vn[i])

    count_li_vn = 0 # đếm số dòng nơi nhận trong file tiếng việt, file tiếng anh không có mục này nên phải để trống
    for elem in main_text_vn_raw:
      if elem.startswith("-"):
        count_li_vn = count_li_vn+1
    
    for elem in main_text_vn_raw:
        if "VỮNG VÀNG TRONG THỬ THÁCH" in elem:
            main_text_vn_raw.remove(elem)
    
    main_text_vn = []
    for elem in main_text_vn_raw:
        elem_fix = preprocess_abbreviations(elem)
        main_text_vn.append(elem_fix)

    bucket_arr_vn = []
    for i in range(0 , len(main_text_vn)):
        sentence = sent_tokenize(main_text_vn[i]) #Tách đoạn thành câu
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
        if len(elem)<4: # xóa những dòng bị thừa
            standardized_arr_vn.remove(elem)
    
    
    standardized_arr_vn = [x for x in standardized_arr_vn if not is_number_comma(x)]
    standardized_arr_vn = [x for x in standardized_arr_vn if not is_number_dot(x)]
    standardized_arr_vn = [x for x in standardized_arr_vn if not is_number_comma_dot(x)]
    standardized_arr_vn = [x for x in standardized_arr_vn if not is_number_comma_percent(x)]
    standardized_arr_vn = [x for x in standardized_arr_vn if not is_number_dot_percent(x)]
    
    

    # Xử lý tiếng anh
    
    text = convert_docx_to_txt(docx_file_path_en)

    namefile_en = docx_file_path_en.split("/")[1].split(".")[0]

    text_arr = text.split("\n")
    main_text_arr_raw = []
    


    for i in range(0 , len(text_arr)): #created and standardized file txt
        if len(text_arr[i])>3:
            text_arr[i] = text_arr[i].strip()
            main_text_arr_raw.append(text_arr[i])

    for elem in main_text_arr_raw:
        if "www.vietnamlaws.com" in elem:
            main_text_arr_raw.remove(elem)
        if "STAND FIRM IN CHALLENGES" in elem:
            main_text_arr_raw.remove(elem)
        if elem == "www.LuatVietnam.vn":
            main_text_arr_raw.remove(elem)
        if "Legal Forum" in elem:
            main_text_arr_raw.remove(elem)
    for elem in main_text_arr_raw:
        if "footnote" in elem:
            main_text_arr_raw.remove(elem)
            
    for i in range(0, len(main_text_arr_raw)):
        if main_text_arr_raw[i].startswith("www.LuatVietnam.vn"):
            main_text_arr_raw[i] = main_text_arr_raw[i].replace("www.LuatVietnam.vn", "")
            
    main_text_arr = []
    for elem in main_text_arr_raw:
        elem_fix = preprocess_abbreviations(elem)
        main_text_arr.append(elem_fix)
          
    bucket_arr_en = []
    for i in range(0 , len(main_text_arr)):
        sentence = sent_tokenize(main_text_arr[i]) #Tách đoạn thành câu
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
        if len(elem)<4: # Xóa những dòng bị thừa
            standardized_arr_en.remove(elem)

    standardized_arr_en = [x for x in standardized_arr_en if not is_number_comma(x)]
    standardized_arr_en = [x for x in standardized_arr_en if not is_number_dot(x)]
    standardized_arr_en = [x for x in standardized_arr_en if not is_number_comma_dot(x)]
    standardized_arr_en = [x for x in standardized_arr_en if not is_number_comma_percent(x)]
    standardized_arr_en = [x for x in standardized_arr_en if not is_number_dot_percent(x)]
    result_en = []
    

    for element in standardized_arr_en:
        if result_en and element.endswith("No."):
            result_en[-1] += element # Append to the last element of result
        else:
            result_en.append(element) # Add a new element to result
        
    for elem in result_en:
        if "www.vietnamlaws.com" in elem:
            result_en.remove(elem)
        if "STAND FIRM IN CHALLENGES" in elem:
            result_en.remove(elem)
        if elem == "www.LuatVietnam.vn":
            result_en.remove(elem)
        if "Legal Forum" in elem:
            result_en.remove(elem)
    for elem in result_en:
        if "footnote" in elem:
            result_en.remove(elem)
    
    final_resul_en = []
    for elem in result_en:
        if 'Article' in elem:
            if "\t" in elem:
                cut_arr = elem.split("\t")
                if len(cut_arr)>1:
                    final_resul_en.append(cut_arr[0])
                    final_resul_en.append(cut_arr[1])
            elif ":" in elem:
                cut_arr = elem.split("\t")
                if len(cut_arr)>1:
                    final_resul_en.append(cut_arr[0])
                    final_resul_en.append(cut_arr[1])
            else:
                final_resul_en.append(elem)
        else:
            final_resul_en.append(elem)
    
    final_resul_vn = []
    for elem in standardized_arr_vn:
        if 'Điều' in elem:
            if "\t" in elem:
                cut_arr = elem.split("\t")
                if len(cut_arr)>1:
                    final_resul_vn.append(cut_arr[0])
                    final_resul_vn.append(cut_arr[1])
            elif ":" in elem:
                cut_arr = elem.split("\t")
                if len(cut_arr)>1:
                    final_resul_vn.append(cut_arr[0])
                    final_resul_vn.append(cut_arr[1])
            else:
                final_resul_vn.append(elem)
        else:
            final_resul_vn.append(elem)

    
    

    with open("./output/"+namefile_en+"_out_en.txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(final_resul_en) + "."
        file_txt.write(string_text) 
    
    with open("./output/"+namefile_vi+"_out_vn.txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(final_resul_vn) + "."
        file_txt.write(string_text) 
    
    
    print("Generate file from "+namefile_en+".docx and "+namefile_vi+".docx"+" success")
        

