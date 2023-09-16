from ast import Import
from pickle import TRUE
import docx2txt
import re
import langid
import string
import sys



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


def checkString(string): # kiểm tra phụ lục
    if string.startswith("Phụ lục"):
        return False
    else:
        return True

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

    # print(namefile)
    textArr = text.split("\n")
    correctArr = []
    bucket_Arr = []

    for i in range(0 , len(textArr)):
        if len(textArr[i])>1: # chuẩn hóa, loại bỏ những dòng rỗng, bị cắt lỗi
            textArr[i] = textArr[i].strip()
            correctArr.append(textArr[i])
    for i in range(0 , len(correctArr)): # chuẩn hóa lại mảng text
        if len(correctArr[i])>1:
            bucket_Arr.append(correctArr[i])

    english_sentences = []
    vietnamese_sentences = []

    index_sign = -1 # Tìm dòng chữ ký
    for i in range (0, len(bucket_Arr)):
      if bucket_Arr[i] == "Date:":
        index_sign = i 
        break 

    for i in range(index_sign+2, len(bucket_Arr)-1): #bắt đầu lấy từ sau dòng chữ ký
        if check_language(bucket_Arr[i]) == "Vietnamese": # kiểm tra xem câu đó có là tiếng việt hay không
            if "/" in bucket_Arr[i]:
                arrcheckString = bucket_Arr[i].split("/")
                if check_language(arrcheckString[0]) == "English" or check_language(arrcheckString[0]) == "Unknown":
                    english_sentences.append(arrcheckString[0])
                    vietnamese_sentences.append(arrcheckString[1])
                else:
                    vietnamese_sentences.append(bucket_Arr[i])
            else:
                if checkString(bucket_Arr[i]):
                    vietnamese_sentences.append(bucket_Arr[i])
        else:
            english_sentences.append(bucket_Arr[i])
    
    for i in range(0 , len(english_sentences)): #chuẩn hóa mảng
        if checkStringStartNumber(english_sentences[i]) or checkStringBullet(english_sentences[i]): # kiểm tra xem có bắt đầu là đề mục không
            english_sentences[i] = english_sentences[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục

    for i in range(0 , len(vietnamese_sentences)):
        if checkStringStartNumber(vietnamese_sentences[i]) or checkStringBullet(vietnamese_sentences[i]): # kiểm tra xem có bắt đầu là đề mục không
            vietnamese_sentences[i] = vietnamese_sentences[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục

    vietnamese_text = "\n".join(vietnamese_sentences) + "." # nối các phần tử của mảng lại với nhau
    english_text = "\n".join(english_sentences) + "."
    with open("./output/out_en_"+namefile+".txt", "w", encoding="utf-8") as file_txt: #in file
        file_txt.write(english_text) 
    with open("./output/out_vi_"+namefile+".txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(vietnamese_text) 
    
    print("Generate file from "+namefile+".docx success")

        

