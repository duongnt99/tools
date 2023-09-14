from ast import Import
from pickle import TRUE
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

def checkStringStartNumber(string):
    if string.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "□")):
        return True
    else:
        return False

if __name__ == '__main__':
    docx_file_path = input("Input file name IFRS(docx): ")#'ifrs.docx'
    text = convert_docx_to_txt("./data/"+docx_file_path)

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
    with open("./output/out_en_ifrs.txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(english_text) 
    with open("./output/out_vi_ifrs.txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(vietnamese_text) 

    print("Done")

   
        

