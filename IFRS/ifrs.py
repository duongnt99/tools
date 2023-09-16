from ast import Import
from pickle import TRUE
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

def checkStringStartNumber(string):
    if string.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "□")):
        return True
    else:
        return False

if __name__ == '__main__':
    # docx_file_path = input("Input file name British Council(docx): ")#'bri.docx'
    # Lấy tên của file python
    script_name = sys.argv[0] # script_name = "process_docx.py"

    # Lấy tên của file docx tiếng Anh
    docx_file_path = sys.argv[1] # en_file = "<filename> (EN).docx"

    # Lấy tên của file docx tiếng Việt
    # vn_file = sys.argv[2] # vn_file = "<filename> (VN).docx"

    # Tiếp tục xử lý hai file docx theo ý bạn
    text = convert_docx_to_txt(docx_file_path)

    namefile = docx_file_path.split("/")[1].split(".")[0] #Lấy tên file

    textArr = text.split("\n")
    correctArr = []

    for i in range(0 , len(textArr)): #created and standardized file txt
        if len(textArr[i])>1:
            textArr[i] = textArr[i].strip()
            correctArr.append(textArr[i])
        
    english_sentences = []
    vietnamese_sentences = []

    for i in range(1, len(correctArr)):
        if i%2==1:
            english_sentences.append(correctArr[i])
        else:
            vietnamese_sentences.append(correctArr[i])

    vietnamese_text = "\n".join(vietnamese_sentences) + "."
    english_text = "\n".join(english_sentences) + "."
    with open("./output/out_en_"+namefile+".txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(english_text) 
    with open("./output/out_vi_"+namefile+".txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(vietnamese_text) 

    print("Generate file from "+namefile+".docx success")

   
        

