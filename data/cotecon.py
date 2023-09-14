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


if __name__ == '__main__':
    # Xử lý tiếng việt
    # docx_file_path_vi = input("Input file name NĐ Vietnamese(docx): ") #'con_vi.docx'
    docx_file_path_vi, docx_file_path_en = input("Input file name Cotecon Vietnamese and English: ").split()
    # docx_file_path_vi = 'con_vi.docx'
    text = convert_docx_to_txt(docx_file_path_vi)

    text_arr_vn = text.split("\n")
    
    main_text_vn = []


    for i in range(0 , len(text_arr_vn)): #created and standardized file txt
      if len(text_arr_vn[i])>1:
        text_arr_vn[i] = text_arr_vn[i].strip()
        main_text_vn.append(text_arr_vn[i])
    
    for elem in main_text_vn:
        if "VỮNG VÀNG TRONG THỬ THÁCH" in elem:
            main_text_vn.remove(elem)
    
    # print(main_text_vn[6])
    
    with open("out_vi_cotecon.txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(main_text_vn) + "."
        file_txt.write(string_text) 


    # Xử lý tiếng anh
    # docx_file_path_en = input("Input file name NĐ English(docx): ")  #'con_en.docx'
    # docx_file_path_en = 'con_en.docx'
    text = convert_docx_to_txt(docx_file_path_en)

    text_arr = text.split("\n")
    main_text_arr = []


    for i in range(0 , len(text_arr)): #created and standardized file txt
        if len(text_arr[i])>1:
            text_arr[i] = text_arr[i].strip()
            main_text_arr.append(text_arr[i])

    for elem in main_text_vn:
        if "STAND FIRM IN CHALLENGES" in elem:
            main_text_vn.remove(elem)
            
    with open("out_en_cotecon.txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(main_text_arr) + "."
        file_txt.write(string_text)
    
    
    
    
    print("Done")
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

