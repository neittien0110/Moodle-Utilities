#!/usr/bin/env python # -- coding: utf-8 
#---------------------------------------------------------------------------------------------
# References:
#   - Thay đổi nội dung xml bằng Beautisoup:
#       https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_modifying_the_tree.htm
#---------------------------------------------------------------------------------------------
from email.policy import default
from tokenize import Number
from bs4 import BeautifulSoup, Comment

#---------------------------------------------------------------------------------------------
#  ENVIRONMENT
#---------------------------------------------------------------------------------------------
QUESTIONARE = "questions-BL-IT4244-132671-GiangVTH-PM-QuestBank-Eng-20220627-0928.xml"
""" Danh sách câu hỏi dạng Moodle XML """

# Phục vụ chuyển đổi cấu trúc thư mục lưu câu hỏi Category bằng cách thay thế,
# giúp không bị lẫn giữa câu hỏi cũ và mới
OLD_CATEGORY="GiangVTH-PM-QuestBank-Eng"
NEW_CATEGORY="GiangVTH-PM-QuestBank-Eng/Dành cho dịch thuật"


TEXT_GUIDE_TOP = 'Hãy dịch nội dung sau sang tiếng Việt. <strong>GIỮ NGUYÊN CẤU TRÚC</strong> và các kí hiệu số <strong><<..>></strong> trong trả lời.'
TEXT_GUIDE_HEADER = '-------------------------CÂU HỎI -------------------------'
TEXT_GUIDE_MIDDLE = '-------------------------LỰA CHỌN-------------------------'
TEXT_GUIDE_FOOTER = '------------------------- GỢI Ý  -------------------------'

OUTPUT_FILE = "essay.xml"

class AnswerStructure:
    text: str
    fraction: Number
    
#---------------------------------------------------------------------------------------------
#  MAIN
#---------------------------------------------------------------------------------------------
contents= open(QUESTIONARE, mode = "r", encoding="utf8").read()
soup = BeautifulSoup(contents,'xml')


#Lấy ra danh sách câu hỏi qua phân tích soup
questions = soup.find_all('question')
print("SỐ CÂU HỎI: " + str(len(questions)))

#Khởi tạo file đầu ra
OutFile = open(OUTPUT_FILE, mode='w', encoding="utf8")
print('<?xml version="1.0" encoding="UTF-8"?>', file=OutFile)
print('<!-- Convert from Moodle XML type, Quizz Questionares to Essay Questionares. Author: TiennND https://github.com/neittien0110 -->', file=OutFile)
print('<quiz>', file=OutFile)
index = 0
for question in questions:
    #--------Nêu thẻ <question> có attr type="category" thì đó không phải câu hỏi
    type = question['type']
    if ( type == "category"):
        mycategory=question.category.text
        mycategory=str(mycategory).replace(OLD_CATEGORY, NEW_CATEGORY)
        tmp = question.category.find('text')    #Do thẻ text, name, string trùng đúng vào tên hàm nên đành phải đi lòng vòng
        tmp.string = mycategory
        #print(category)
        #category này sẽ áp dụng cho tất cả câu hỏi phía sau, trừ phi có thay đổi
        print(question, file=OutFile)
        continue

    index = index + 1
    #--------Câu hỏi
    ques = question.questiontext.text.strip()
    #--------Gợi ý
    feedback = question.generalfeedback.text.strip()
    #--------Các câu trả lời và đáp án đúng
    ans = list()
    for answers in question.find_all('answer'):
        tmp = AnswerStructure()
        tmp.text = answers.text.strip()
        tmp.fraction =answers["fraction"]
        ans.append(tmp)
    
    
    #------Biến đổi cấu trúc question từ dạng Quiz thành Essay--------------------
    question["type"] = "essay"
    
    #Do thẻ text, name, string trùng đúng vào tên hàm nên đành phải đi lòng vòng
    tmp = question.questiontext.find('text')  
    tmp.string = TEXT_GUIDE_TOP + "<br/>" + TEXT_GUIDE_HEADER + "<br/><<0>>" + ques +   TEXT_GUIDE_MIDDLE + '<br/><<1>>. ' + ans[0].text + '<<2>>. ' + ans[1].text + '<<3>>.'  + ans[2].text + '<<4>>. '  + ans[3].text + TEXT_GUIDE_FOOTER + '<br/><<5>> "' + feedback
    #question.questiontext.string = TEXT_GUIDE_HEADER + '<br/>' + ques + '<br/>' +  TEXT_GUIDE_MIDDLE + '<br/> 1. ' + ans[0].text + '<br/> 2. ' + ans[1].text + '<br/> 3.'  + ans[2].text + '<br/> 4. '  + ans[3].text + '<br/>' + TEXT_GUIDE_FOOTER 
    
    question.penalty.string = "0.0000000"  # Không quan trọng lắm
   
    new_tag = soup.new_tag("responseformat")
    new_tag.string = "editor"
    question.append(new_tag)    
    
    new_tag = soup.new_tag("responserequired")
    new_tag.string = "1"
    question.append(new_tag)    
    
    new_tag = soup.new_tag("responsefieldlines")        # Số dòng để trống cho phần editor
    new_tag.string = "25"
    question.append(new_tag)
    
    
    print(question, file = OutFile)
    print("",file = OutFile)
    #if index == 1:
    #    break;

# In thẻ kết thức
print('</quiz>', file=OutFile)
OutFile.close();
exit(0)
