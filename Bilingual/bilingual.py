from ast import Import
from distutils import core
from math import remainder
from pickle import TRUE
import docx2txt
import re
import langid
import string
import sys
import zipfile
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException # nhập lớp LangDetectException
from underthesea import sent_tokenize

DetectorFactory.seed = 0 # Để kết quả xác định ngôn ngữ là nhất quán, hàm này trả về 3 kết quả: vietnamese, english, unknown. Hầu như unknow đều là tiếng anh, trừ một số trường hợp đặc biệt
def check_language(string):
    try:
        lang = detect(string) # Trả về mã ngôn ngữ theo chuẩn ISO 639-1
        if lang == "en":
            return "English"
        elif lang == "vi":
            return "Vietnamese"
        else:
            return "Unknown"
    except LangDetectException as e:
        # print(f"Lang detect failed for: '{string}'") # in ra giá trị của string khi bắt được lỗi
        return "Unknown" # gán một giá trị mặc định cho ngôn ngữ của string
    
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

def is_upper_or_not_letter(string):
  """
  Kiểm tra xem string chỉ có chữ in hoa hay không.

  Args:
    string: String cần kiểm tra.

  Returns:
    True nếu string chỉ có chữ in hoa, False nếu không.
  """

  return all(
      c.isupper() or not c.isalpha() for c in string
  )


def convert_docx_to_txt(docx_file_path):
    try:
        with open(docx_file_path, 'rb') as docx_file:
            text = docx2txt.process(docx_file)
        return text
    except zipfile.BadZipFile:
        return f"Error: {docx_file_path} is not a valid zip file."

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
    main_text = []

    for i in range(0 , len(textArr)): #created and standardized file txt
        if len(textArr[i])>3:
            textArr[i] = textArr[i].strip()
            main_text.append(textArr[i])
    
    bucket_arr = []
    for i in range(0 , len(main_text)):
            sentence = sent_tokenize(main_text[i]) #Tách đoạn thành câu
            bucket_arr.append(sentence)
    

    correctArr = []
    for i in range (0,len(bucket_arr)):
        if(len(bucket_arr[i])>1): # tìm đoạn văn
            for j in range(0, len(bucket_arr[i])):
                correctArr.append(bucket_arr[i][j]) # Lấy các câu trong đoạn văn
        else:
            string_text = "".join(bucket_arr[i])
            correctArr.append(string_text) #lấy các câu đơn
    
    for elem in correctArr:
        if len(elem)<4: # xóa những dòng bị thừa
            correctArr.remove(elem)

    correctArr = [x for x in correctArr if not is_number_comma(x)]
    correctArr = [x for x in correctArr if not is_number_dot(x)]
    correctArr = [x for x in correctArr if not is_number_comma_dot(x)]
    correctArr = [x for x in correctArr if not is_number_comma_percent(x)]
    correctArr = [x for x in correctArr if not is_number_dot_percent(x)]

    for i in range(0 , len(correctArr)):
        if checkStringStartNumber(correctArr[i]): # kiểm tra xem có bắt đầu là đề mục không
            correctArr[i] = correctArr[i].split(" ", 1)[1].strip() #lấy phần tử thứ 2, loại bỏ đề mục

    english_sentences = []
    vietnamese_sentences = []
    
    
    
    # text = 'sử'
    # print(text)
    # print(check_language(text))
    # english_sentences_part = ""
    # vietnamese_sentences_part = ""
    # tempArrUnknown = text.split(" ") # cut string if contains /
    # for sentence in tempArrUnknown:
    #     print(sentence)
    #     print(check_language(sentence))
    #     if (check_language(sentence)=="Vietnamese" or sentence=='Rút' or 'HÀNG HÓA' in sentence or 'GIÁ' in sentence) and ('VALIDITY' not in sentence):
    #         vietnamese_sentences_part+=sentence+" " # merge string after check language
    #     else:
    #         english_sentences_part+=sentence+" "
    # vietnamese_sentences.append(vietnamese_sentences_part)
    # english_sentences.append(english_sentences_part)
    # print(english_sentences)
    # print(vietnamese_sentences)

    for i in range(0, len(correctArr)):
        english_sentences_part = ""
        vietnamese_sentences_part = ""
        if check_language(correctArr[i])=="Vietnamese":
            if "/" in correctArr[i]:
                tempArr = correctArr[i].split("/") # cut string if contains /
                for sentence in tempArr:
                    if check_language(sentence)=="Vietnamese" and 'VALIDITY' not in sentence: 
                        vietnamese_sentences_part+=sentence+" " # merge string after check language
                    else:
                        english_sentences_part+=sentence+" "
                vietnamese_sentences.append(vietnamese_sentences_part)
                english_sentences.append(english_sentences_part)
            
            elif "." in correctArr[i]:
                tempArr = correctArr[i].split(".") # cut string if contains /
                for sentence in tempArr:
                    if check_language(sentence)=="Vietnamese" and ('VALIDITY' and 'ElectronicdocumentsrelatingtotheServiceincludingOrdersforpayment' and 'Customer') not in sentence: 
                        vietnamese_sentences_part+=sentence+" " # merge string after check language
                    else:
                        english_sentences_part+=sentence+" "
                vietnamese_sentences.append(vietnamese_sentences_part)
                english_sentences.append(english_sentences_part)

            elif ";" in correctArr[i]:
                tempArr = correctArr[i].split(";") # cut string if contains /
                for sentence in tempArr:
                    if check_language(sentence)=="Vietnamese" and ('VALIDITY' and 'Thirdpartiesareorganizationsthatprovidee') not in sentence: 
                        vietnamese_sentences_part+=sentence+" " # merge string after check language
                    else:
                        english_sentences_part+=sentence+" "
                vietnamese_sentences.append(vietnamese_sentences_part)
                english_sentences.append(english_sentences_part)

            elif ":" in correctArr[i]:
                tempArr = correctArr[i].split(":") # cut string if contains /
                for sentence in tempArr:
                    if check_language(sentence)=="Vietnamese" and 'VALIDITY' not in sentence: 
                        vietnamese_sentences_part+=sentence+" " # merge string after check language
                    else:
                        english_sentences_part+=sentence+" "
                vietnamese_sentences.append(vietnamese_sentences_part)
                english_sentences.append(english_sentences_part)
            

            else:
                vietnamese_sentences.append(correctArr[i])

            
            
        else:
            if "/" in correctArr[i]: #Unknown case
                tempArrUnknown = correctArr[i].split("/") # cut string if contains /
                for sentence in tempArrUnknown:
                    if check_language(sentence)=="Vietnamese" or sentence=='Rút' or 'HÀNG HÓA' in sentence or 'GIÁ' in sentence:
                        vietnamese_sentences_part+=sentence+" " # merge string after check language
                    else:
                        english_sentences_part+=sentence+" "
                vietnamese_sentences.append(vietnamese_sentences_part)
                english_sentences.append(english_sentences_part)
            
            elif "." in correctArr[i]: #Unknown case
                tempArrUnknown = correctArr[i].split(".") # cut string if contains /
                for sentence in tempArrUnknown:
                    if check_language(sentence)=="Vietnamese" or sentence=='Rút' or 'HÀNG HÓA' in sentence or 'GIÁ' in sentence:
                        vietnamese_sentences_part+=sentence+" " # merge string after check language
                    else:
                        english_sentences_part+=sentence+" "
                vietnamese_sentences.append(vietnamese_sentences_part)
                english_sentences.append(english_sentences_part) 
            
            elif ";" in correctArr[i]: #Unknown case
                tempArrUnknown = correctArr[i].split(";") # cut string if contains /
                for sentence in tempArrUnknown:
                    if check_language(sentence)=="Vietnamese" or sentence=='Rút' or 'HÀNG HÓA' in sentence or 'GIÁ' in sentence:
                        vietnamese_sentences_part+=sentence+" " # merge string after check language
                    else:
                        english_sentences_part+=sentence+" "
                vietnamese_sentences.append(vietnamese_sentences_part)
                english_sentences.append(english_sentences_part)
            
            elif ":" in correctArr[i]: #Unknown case
                tempArrUnknown = correctArr[i].split(":") # cut string if contains /
                for sentence in tempArrUnknown:
                    if check_language(sentence)=="Vietnamese" or sentence=='Rút' or 'HÀNG HÓA' in sentence or 'GIÁ' in sentence:
                        vietnamese_sentences_part+=sentence+" " # merge string after check language
                    else:
                        english_sentences_part+=sentence+" "
                vietnamese_sentences.append(vietnamese_sentences_part)
                english_sentences.append(english_sentences_part) 
            

            else:
                english_sentences.append(correctArr[i])
    
    for elem in vietnamese_sentences:
        if len(elem)<4:
            vietnamese_sentences.remove(elem)
    for elem in english_sentences:
        if len(elem)<4:
            english_sentences.remove(elem)
    
    for elem in vietnamese_sentences:
        if "ĐIỀU KIỆN CHUNG-NGÂN HÀNG TNHH CTBC" in elem:
            vietnamese_sentences.remove(elem)
        if 'LBVN' in elem and len(elem)<10:
            vietnamese_sentences.remove(elem)
        if 'General' in elem or 'Definitions'in elem or 'for HLB Connect'in elem or 'Computer Terminal'in elem or 'Biometric'in elem or 'Setting' in elem or 'Set up'in elem or 'Change'in elem or 'Un-enroll'in elem or 'Un-active'in elem or 'Risk'in elem or 'Online'in elem or 'Manage'in elem or 'Placement'in elem or 'Balances'in elem or 'Frequently'in elem or 'Information'in elem or 'transfer'in elem or 'Availability'in elem or 'Instructions'in elem or 'Transaction'in elem or 'Services'in elem or 'Service'in elem or 'Responsibilities'in elem or 'Security'in elem or 'Liabilities'in elem or 'Suspension'in elem or 'Consent'in elem or 'Disclosure'in elem or 'Reconstruction'in elem or 'Enquiries'in elem or 'Governing'in elem or 'Indemnity' in elem: 
            vietnamese_sentences.remove(elem)
        if 'MB04-QT.TDC 124' in elem:
            vietnamese_sentences.remove(elem)
        if 'HLBVN_FA(VEHICLE)_CO' in elem:
            vietnamese_sentences.remove(elem)
        
    for elem in english_sentences:
        if "Connect Aug’22" in elem:
            english_sentences.remove(elem)
        if ("nghĩa" or 'thích' or 'hoặc' or 'and Internet Mobile Network' or 'cập' or 'ký') in elem:
            english_sentences.remove(elem)
        if 'JOINT FD AGT_JUL’19' in elem:
            english_sentences.remove(elem)
        if 'Part A Nov’22 V3' in elem:
            english_sentences.remove(elem)
        if 'HLBVN_FA(VEHICLE)' in elem:
            english_sentences.remove(elem)
        if 'hongleongconnect' in elem and len(elem)< 30:
            english_sentences.remove(elem)

    if "/cskh.hafelevietnam.com.vn/" in english_sentences:
        english_sentences.remove("/cskh.hafelevietnam.com.vn/")
    if "fax/zalo/" in english_sentences:
        english_sentences.remove("fax/zalo/")
    if "Page 1 of 3" in english_sentences:
        english_sentences.remove("Page 1 of 3")
    if "Page 2 of 3" in english_sentences:
        english_sentences.remove("Page 2 of 3")
    if "Page 3 of 3" in english_sentences:
        english_sentences.remove("Page 3 of 3")


    for elem in vietnamese_sentences:
        if len(elem)<3:
            vietnamese_sentences.remove(elem)
    for elem in english_sentences:
        if len(elem)<3:
            english_sentences.remove(elem)
    
    vietnamese_text = "\n".join(vietnamese_sentences) + "."
    english_text = "\n".join(english_sentences) + "."
    with open("./output/out_en_"+namefile+".txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(english_text) 
    with open("./output/out_vi_"+namefile+".txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(vietnamese_text) 

    print("Generate file from "+namefile+".docx success")
    
