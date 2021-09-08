import json
import pdfbox
import os
from PY_Dictionary import dict_replace
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

def text_ocr():
    p = pdfbox.PDFBox()
    list_files1, list_files2, list_files3 = [], [], []
    path = "F:\_PythonNLP\paper"
    des_path = "F:\_PythonNLP\paper\ex_regex"
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.pdf'):
                list_files1.append(os.path.join(root, file))          # PATH with .PDF
                new_file = file.replace('.pdf', '.txt')
                list_files2.append(os.path.join(root, new_file))      # PATH with .txt
                list_files3.append(os.path.join(des_path, new_file))  # NEW PATH with .txt
    for f in list_files1:
        p.extract_text(f, encoding='UTF-8')
    for f1, f2 in zip(list_files2, list_files3):                      # Move file to New Dir
        move(f1, f2)
    for t in list_files3:
        replace_correct(t)
    list_files1.clear()                                               # Clear the list
    list_files2.clear()
    list_files3.clear()


def replace_correct(file_path):
    label = ['ค', 'ง', 'จ', 'ฉ', 'ช', 'ซ', 'ฌ', 'ญ', 'ฎ', 'ฏ', 'ฐ', 'ฑ', 'ฒ', 'ณ', 'ด', 'ต', 'ถ', 'ท', 'ธ']
    label = [('\n' + x + ' \n') for x in label]
    chapter = list(map(str, range(1, 10)))
    chapter = [('\nบทที่' + x + ' \n') for x in chapter]
    special = ['\nเอกสารอ้างอิง \n', '\nเอกสารอ้างอิง (ต่อ) \n', '\nประวัติผู้แต่ง \n']
    label = label + chapter + special             # ['\nค \n', '\nง \n', '\nจ \n', ... '\nบทที่1 \n', '\nบทที่2 \n', ... '\nเอกสารอ้างอิง \n', '\nเอกสารอ้างอิง (ต่อ) \n',  '\nประวัติผู้แต่ง \n']

    fh, abs_path = mkstemp()                      # Create Temp file
    with fdopen(fh, 'w', encoding='UTF-8') as new_file:
        with open(file_path, encoding='UTF-8') as old_file:
            paper = ''.join(old_file.readlines())
            paper = dict_replace(paper)
        for i in label:
            if i in paper:
                paper = paper.replace(i, '\n######' + i.replace('\n', '') + '\n')

        new_file.write(paper)
    copymode(file_path, abs_path)                 # Copy the file permissions from the old file to the new file
    remove(file_path)                             # Remove original file
    move(abs_path, file_path)                     # Move new file


def chapter_list():                               # In TESTING
    with open('F:\_PythonNLP\paper\ex_regex\paper001.txt', 'r', encoding='UTF-8') as file:
        text = ''.join(file.readlines())
        ch = text.split('######')
        with open('F:/_PythonNLP/paper/JSON/test.json', 'w', encoding='UTF-8') as f:
             json.dump(ch, f, ensure_ascii=False, indent = 4)


#text_ocr()
#chapter_list()



