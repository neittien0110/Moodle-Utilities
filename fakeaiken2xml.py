#!/usr/bin/env python # -- coding: utf-8 
#---------------------------------------------------------------------------------------------
# References:
#---------------------------------------------------------------------------------------------
from email.policy import default
from tokenize import Number
import re

#---------------------------------------------------------------------------------------------
#  ENVIRONMENT
#---------------------------------------------------------------------------------------------
MULTICHOICE_TEMPLATE=' \
<question type="multichoice">          \n \
    <name>          \n \
      <text>_name_</text>          \n \
    </name>          \n \
    <questiontext format="plain_text">          \n \
      <text>_text_</text>          \n \
    </questiontext>          \n \
    <generalfeedback format="plain_text">          \n \
      <text></text>          \n \
    </generalfeedback>          \n \
    <defaultgrade>1.0000000</defaultgrade>          \n \
    <penalty>0.3333333</penalty>          \n \
    <hidden>0</hidden>          \n \
    <idnumber></idnumber>          \n \
    <single>true</single>          \n \
    <shuffleanswers>true</shuffleanswers>          \n \
    <answernumbering>abc</answernumbering>          \n \
    <showstandardinstruction>0</showstandardinstruction>          \n \
    <correctfeedback format="html">          \n \
      <text></text>          \n \
    </correctfeedback>          \n \
    <partiallycorrectfeedback format="html">          \n \
      <text></text>          \n \
    </partiallycorrectfeedback>          \n \
    <incorrectfeedback format="html">          \n \
      <text></text>          \n \
    </incorrectfeedback>          \n \
    <answer fraction="_fraction0_" format="plain_text">          \n \
      <text>_ans0_</text>          \n \
      <feedback format="html">          \n \
        <text></text>          \n \
      </feedback>          \n \
    </answer>          \n \
    <answer fraction="_fraction1_" format="plain_text">          \n \
      <text>_ans1_</text>          \n \
      <feedback format="html">          \n \
        <text></text>          \n \
      </feedback>          \n \
    </answer>          \n \
    <answer fraction="_fraction2_" format="plain_text">          \n \
      <text>_ans2_</text>          \n \
      <feedback format="html">          \n \
        <text></text>          \n \
      </feedback>          \n \
    </answer>          \n \
    <answer fraction="_fraction3_" format="plain_text">          \n \
      <text>_ans3_</text>          \n \
      <feedback format="html">          \n \
        <text></text>          \n \
      </feedback>          \n \
    </answer>          \n \
  </question>           \n \
  <!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->\n\n   \
  '   
def XML_Encoding(text):
  return text.replace("&","&amp;").replace("'","&apos;").replace('"',"&quot;").replace("<","&lt;").replace(">","&gt;")  
#---------------------------------------------------------------------------------------------
#  MAIN
#---------------------------------------------------------------------------------------------

import csv
import sys

def DetectOptionMarker(text):
  """Hiệu chỉnh kiểu đánh dấu các lựa chọn
     Cú pháp chính xác: "A) " hoặc "B) " và phải ở đầu của mỗi dòng
     Tuy nhiên tình huống thường gặp là "A. " hoặc "C. "
  """
  return re.sub("^([A-D])+['.'][' ','\t']","\\1) ",text, flags=re.MULTILINE)

def Help():
  print("Convert from half fake Aiken format with the multi-line question content to the Moodle XML format")
  print("Syntax: ")
  print("        python ./fakeaiken2xml.py <aikenfile> [title prefix] [the start number of title indexing]")
  print("Example:")
  print(" python ./fakeaiken2xml.py question1.txt ")
  print(" python ./fakeaiken2xml.py question2.txt listening_task1_ ")
  print(" python ./fakeaiken2xml.py question3.txt writing_task2_ 1031")


Help()
input_file = sys.argv[1]
count_from = 0
if len(sys.argv) > 2:
  title_prefix = sys.argv[2]
  if len(sys.argv) > 3:
    count_from = int(sys.argv[3])
  else:
    count_from = 1
else:
  title_prefix = ""

#input_file = '.\\newimport\\SoanCauHoiTHDC_20212_NguyenHongQuang\\S5_NguyenHongQuang.txt'
output_file = input_file + ".xml"

input = open(input_file, mode = "r" , encoding = "utf_8")
allcontent = input.read()
allcontent = DetectOptionMarker(allcontent)
#print(allcontent)

# Đọc toàn bộ ngân hàng câu hỏi gốc
output= open(output_file, mode = "w", encoding="utf8")
xmlQuestion = MULTICHOICE_TEMPLATE

#Khởi tạo file đầu ra
output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
output.write('<!-- Convert from Moodle XML type. Essay Questionares + Essay Responses ==> output. Author: TiennND https://github.com/neittien0110 -->\n')
output.write('<quiz>\n')

question = ""
ans = ['','','','']
fraction=[0,0,0,0,0]

count = count_from - 1
for line in allcontent.splitlines():
    row = line.rstrip("\n").rstrip("\r")   
    Keyword = line[0:3]
    index = -1
    if Keyword == "A) ":
      index = 0
    elif  Keyword == "B) ":
      index = 1
    elif Keyword == "C) ":
      index = 2
    elif Keyword == "D) " :  
      index = 3
    elif Keyword == "ANS":
      if ans[3] == '1016':
        pass
      selector = ord(line[8:9])-65
      if (selector >=4) or (selector < 0):
        print("ERROR: something wrong in the following line: " + line)
        break
      fraction[selector] = 100
    else:

        question =  question + row + "\n"
    if index >= 0:
        ans[index] = row[3:] 
    
    # Kết thúc trọn vẹn câu hỏi, ghi kết quả chuyển đổi vào file xml    
    if Keyword == "ANS":
      count=count+1
      print(question)
      print(str(fraction[0]).zfill(3) + " | " + ans[0])
      print(str(fraction[1]).zfill(3) + " | " + ans[1])
      print(str(fraction[2]).zfill(3) + " | " + ans[2])
      print(str(fraction[3]).zfill(3) + " | " + ans[3])

      
      question = XML_Encoding(question.strip("\n").strip("\r").strip(""))
      
      
      xmlQuestion=xmlQuestion.replace("_text_", question)
      title = question.split('\n', 1)[0]   
      if (title_prefix != ""):
        title =  title_prefix + str(count).zfill(3) + " " + title
      print(title)
      print()     
      print()                 
      xmlQuestion=xmlQuestion.replace("_name_", title)      
      for i in range(0,4):
        xmlQuestion=xmlQuestion.replace("_fraction" + str(i) +"_", str(fraction[i]))
        xmlQuestion=xmlQuestion.replace("_ans" + str(i) +"_", XML_Encoding(ans[i]))
      output.write(xmlQuestion)
        
      question = ""
      fraction=[0,0,0,0]
      ans = ['','','','']
      xmlQuestion = MULTICHOICE_TEMPLATE

output.write("</quiz>")
output.close()

exit(0)


