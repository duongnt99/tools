from ast import Import
from os import remove
from pickle import TRUE
from unittest import result
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
def checkStringBullet(string): # kiểm tra đầu mục có bắt đầu bằng dấu ()
    if string.startswith("("):
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
    docx_file_path_vi, docx_file_path_en = input("Input file name Woori Vietnamese and English: ").split() #'woori_vi.docx'
    # docx_file_path_vi = 'woori_vi.docx'
    text_vn = convert_docx_to_txt(docx_file_path_vi)

    text_arr_vn = text_vn.split("\n")
    
    main_text_vn = []


    for i in range(0 , len(text_arr_vn)): #created and standardized file txt
      if len(text_arr_vn[i])>1:
        text_arr_vn[i] = text_arr_vn[i].strip()
        main_text_vn.append(text_arr_vn[i])

    final_arr_vn = []
    
    for i in range (0, len(main_text_vn)):
        if checkStringStartNumber(main_text_vn[i]):
            sentence = []
            correct_text_arr = main_text_vn[i].split(".")
            if(correct_text_arr[2].isnumeric()):
                for i in range(3, len(correct_text_arr)):
                    sentence.append(correct_text_arr[i])
            else:
                for i in range(2, len(correct_text_arr)):
                    sentence.append(correct_text_arr[i])

            correct_text = "".join(sentence)
            final_arr_vn.append(correct_text)
        else:
            correct_text = main_text_vn[i]
            final_arr_vn.append(correct_text)

    for i in range(0 , len(final_arr_vn)):
        if checkStringStartNumber(final_arr_vn[i]) or checkStringBullet(final_arr_vn[i]): # kiểm tra xem có bắt đầu là đề mục không
            final_arr_vn[i] = final_arr_vn[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục

    with open("out_vi_woori.txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(final_arr_vn) + "."
        file_txt.write(string_text) 


    # Xử lý tiếng anh
    # docx_file_path_en = input("Input file name Woori English(docx): ")  #'woori_en.docx'
    # docx_file_path_en = 'woori_en.docx'
    text_en = convert_docx_to_txt(docx_file_path_en)

    text_arr_en = text_en.split("\n")
    main_text_arr = []

    for i in range(0 , len(text_arr_en)): #created and standardized file txt
        if len(text_arr_en[i])>1:
            text_arr_en[i] = text_arr_en[i].strip()
            main_text_arr.append(text_arr_en[i])

    final_arr_en = []
    
    for i in range (0, len(main_text_arr)):
        if checkStringStartNumber(main_text_arr[i]):
            sentence = []
            correct_text_arr = main_text_arr[i].split(".")
            if(correct_text_arr[2].isnumeric()):
                for i in range(3, len(correct_text_arr)):
                    sentence.append(correct_text_arr[i])
            else:
                for i in range(2, len(correct_text_arr)):
                    sentence.append(correct_text_arr[i])

            correct_text = "".join(sentence)
            final_arr_en.append(correct_text)
        else:
            correct_text = main_text_arr[i]
            final_arr_en.append(correct_text)

    for i in range(0 , len(final_arr_en)):
        if checkStringStartNumber(final_arr_en[i]) or checkStringBullet(final_arr_en[i]): # kiểm tra xem có bắt đầu là đề mục không
            final_arr_en[i] = final_arr_en[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục

    with open("out_en_woori.txt", "w", encoding="utf-8") as file_txt:
        string_text = "\n".join(final_arr_en) + "."
        file_txt.write(string_text) 

    print("Done!")
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

