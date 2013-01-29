#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import hashlib
import os.path

DEBUG = False
if DEBUG:
    import pdb 
    pdb.set_trace()

CODEC = 'utf-8'
EXT = '.php'
src_php = 'Gangs'
#reg = r'<text>.*?([\u4e00-\u9fa5]+).*?<\/text>'
#reg = r'(.*?<text>.*?)([\x80-\xff]+)(.*?<\/text>.*?)'
#reg = r'(.*?<text>|<text><!\[CDATA\[)(.+?)(<\/text>|\]\]><\/text>.*?)'
#reg = r'(.*?<text>)(.+?)(<\/text>.*?)'
#reg = r"(.*?TEXT\s=\s)('.+?')(.*?)"
reg = r"(.*?,\s*?)(ErrorCode::.+?_TEXT)(.*?)"

def parseFile(filename):
    try:
        try:
            f = open(filename+EXT, 'r')
            content = [line for line in f.readlines()]
            new_content = []
            fn = open('dst_'+filename+EXT, 'w')

            for text in content:
                m = re.match(reg, text)
                if m:
                    tmpStr = re.sub(reg, m.group(1) + 'Language::GetText(' + m.group(2) + ')' + m.group(3), text) # 替换原的中文
                    new_content.append(tmpStr)
                else:
                    new_content.append(text)
            for line in new_content:
                fn.write(line)
        finally:
            if f:
                f.close()
            if fn:
                fn.close()
        print 'Export data successfully.'
    except IOError, e:
        print 'open file error:', filename, e

def exportData():
    filename = raw_input('请输入需要处理的文件名：')
    if not filename:
        filename = src_php
    parseFile(filename)

if __name__ == '__main__':    
    exportData()
