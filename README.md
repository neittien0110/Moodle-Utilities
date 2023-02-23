# Moodle Utilities

## quiz2essay.py

Convert the questionnaire exported Moodle from quiz type to essay type.  
Allow change from an old category name to a new name
Input: Moodle XML file  (built-in code parameter QUESTIONARE )
Output: Moodle XML file (built-in code parameter OUTPUT_FILE )

## fakeaiken2xml.py

- Convert from half fake Aiken format with the multi-line question content to the Moodle XML format.
- Autocorrect to the mistake A.  B. (the correct syntaxt is A)  B))

- Syntax:
    python **./fakeaiken2xml.py** < aikenfile > [title prefix] [the start number of title indexing]

```dos
   python ./fakeaiken2xml.py question1.txt 
   python ./fakeaiken2xml.py question2.txt listening_task1_ 
   python ./fakeaiken2xml.py question3.txt writing_task2_ 1031
```
  
- For example:

```yml
question line 1
question line 2
question line 3
A) option 1
B) option 2
C) option 3
D) option 4
ANSWER: C
```

 The half-fake aiken above is converted to the XML below:

```xml
<question type="multichoice">          
     <name>          
       <text>question line 1</text>          
     </name>          
     <questiontext format="plain_text">          
       <text>
            question line 1
            question line 2
            question line 3
        </text>          
     </questiontext>          
     <generalfeedback format="plain_text">          
       <text></text>          
     </generalfeedback>          
     <defaultgrade>1.0000000</defaultgrade>          
     <penalty>0.3333333</penalty>          
     <hidden>0</hidden>          
     <idnumber></idnumber>          
     <single>true</single>          
     <shuffleanswers>true</shuffleanswers>          
     <answernumbering>abc</answernumbering>          
     <showstandardinstruction>0</showstandardinstruction>          
     <correctfeedback format="html">          
       <text></text>          
     </correctfeedback>          
     <partiallycorrectfeedback format="html">          
       <text></text>          
     </partiallycorrectfeedback>          
     <incorrectfeedback format="html">          
       <text></text>          
     </incorrectfeedback>          
     <answer fraction="0" format="plain_text">          
       <text>option 1</text>          
       <feedback format="html">          
         <text></text>          
       </feedback>          
     </answer>          
     <answer fraction="0" format="plain_text">          
       <text>option 2</text>          
       <feedback format="html">          
         <text></text>          
       </feedback>          
     </answer>          
     <answer fraction="100" format="plain_text">          
       <text>option 3</text>          
       <feedback format="html">          
         <text></text>          
       </feedback>          
     </answer>          
     <answer fraction="0" format="plain_text">          
       <text>option 4</text>          
       <feedback format="html">          
         <text></text>          
       </feedback>          
     </answer>          
   </question>   
```