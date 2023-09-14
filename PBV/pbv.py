from ast import Import
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

def checkStringStartNumber(string):
    if string.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "□")):
        return True
    else:
        return False

if __name__ == '__main__':
    docx_file_path = input("Input file name PBV(docx): ")#'pbv.docx'
    text = convert_docx_to_txt(docx_file_path)

    textArr = text.split("\n")
    correctArr = []

    for i in range(0 , len(textArr)): #created and standardized file txt
        if len(textArr[i])>1:
            textArr[i] = textArr[i].strip()
            correctArr.append(textArr[i])
    for i in range(0 , len(correctArr)):
        if checkStringStartNumber(correctArr[i]): # kiểm tra xem có bắt đầu là đề mục không
            correctArr[i] = correctArr[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục
   

    english_sentences = []
    vietnamese_sentences = []

    for i in range(0, len(correctArr)):
        english_sentences_part = ""
        vietnamese_sentences_part = ""
        if check_language(correctArr[i])=="Vietnamese":
            if "/" in correctArr[i]:
                tempArr = correctArr[i].split("/") # cut string if contains /
                for sentence in tempArr:
                    if check_language(sentence)=="Vietnamese": 
                        vietnamese_sentences_part+=sentence+"/" # merge string after check language
                    else:
                        english_sentences_part+=sentence+"/"
                vietnamese_sentences.append(vietnamese_sentences_part)
                english_sentences.append(english_sentences_part)
            else:
                vietnamese_sentences.append(correctArr[i])
        else:
            if "/" in correctArr[i]: #Unknown case
                tempArrUnknown = correctArr[i].split("/") # cut string if contains /
                english_sentences.append(tempArrUnknown[0])
                vietnamese_sentences.append(tempArrUnknown[1])
            else:
                english_sentences.append(correctArr[i])

    vietnamese_text = "\n".join(vietnamese_sentences) + "."
    english_text = "\n".join(english_sentences) + "."
    with open("out_en.txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(english_text) 
    with open("out_vi.txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(vietnamese_text) 

    print("Done")

        

