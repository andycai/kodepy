#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
从 xml 中提取需要翻译的中文，生产ini文件和中间xml文件
翻译完成后转换成ini文件，然后从ini文件更新中间文件，中间文件就成了翻译后目标文件
Export 表示从源文件中导出需要翻译的文件，并生产ini和中间xml文件
Import 表示从翻译好的ini文件导入文字到中间xml文件中
ini格式：
d9ac9228e8564657bbe9ca5359f95806=创建
625fb26b4b3340f7872b411f401e754c=取消
中间xml文件：
<text>625fb26b4b3340f7872b411f401e754c</text>
<text>625fb26b4b3340f7872b411f401e754c</text>
@version 1.0
'''

import re
import hashlib
import os.path

DEBUG = False
if DEBUG:
    import pdb 
    pdb.set_trace()

CODEC = 'utf-8'
src_xml = './skin.xml'      # 源文件
dst_ini = './skin.ini'      # 导出的ini文件
dst_xml = './export.xml'    # 导出的中间文件
dst_csv = './skin.csv'
start_num = 1000;
start_str = 'xxfy_'
#reg = r'<text>.*?([\u4e00-\u9fa5]+).*?<\/text>'
#reg = r'(.*?<text>.*?)([\x80-\xff]+)(.*?<\/text>.*?)'
#reg = r'(.*?<text>|<text><!\[CDATA\[)(.+?)(<\/text>|\]\]><\/text>.*?)'
reg = r'(.*?<text>)(.+?)(<\/text>.*?)'

def parseFile(filename):
    global fn, fcsv
    try:
        try:
            f = open(filename, 'r')
            content = [line for line in f.readlines()]
            new_content = []
            fo = open(dst_ini, 'r+')
            tmpContent = str(fo.read()).strip()
            fo.seek(0)
            fo.truncate(0)
            if len(tmpContent)>0:
                fo.write(tmpContent + '\n[newSkin]\n');
            else:
                fo.write('[skin]\n')
            for text in content:
                m = re.match(reg, text)
                if m:
                    uniqueStr = hashlib.md5(m.group(2)).hexdigest()
                    tmpStr = re.sub(reg, m.group(1) + uniqueStr + m.group(3), text) # 替换原的中文
                    new_content.append(tmpStr)
                    if tmpContent.find(uniqueStr)==-1:    # 已经存在不要加入
                        fo.write(uniqueStr + '=' + m.group(2) +'\n')
                    fcsv.write(uniqueStr + ',"' + m.group(2) +'"\n')
                else:
                    new_content.append(text)
            for line in new_content:
                fn.write(line)
        finally:
            if f:
                f.close()
            if fo:
                fo.close()
        print 'Export data successfully.'
    except IOError, e:
        print 'open file error:', filename, e

def exportData():
    global fn, fcsv
    filename = raw_input('''
Input your file path such as '/home/andy/skin.xml', 'skin.xml' and so on.
'skin.xml' is default file if nothing input.
Files 'skin.ini' and 'export.xml' will be exported finally. 
''')
    try:
        fn = open(dst_xml, 'w+')
        fcsv = open(dst_csv, 'w+')
        if (filename):
            if os.path.isfile(filename):
                parseFile(filename)
            else:
                raise IOError('file ' + filename + ' has not exists.')
        else:
            parseFile(src_xml)
    except IOError, e:
        print e
    finally:
        if fn:
            fn.close()
        if fcsv:
            fcsv.close()

def importData():
    import ConfigParser
    
    cf = ConfigParser.ConfigParser()
    cf.read(dst_ini)
    s = cf.items('skin')
    f = open(dst_xml, 'r+')
    content = str(f.read())
    for key, value in s:
        content = content.replace(key, value)
    f.seek(0)
    f.truncate(0)
    f.write(content)
    f.close
    print 'Import data successfully.'

if __name__ == '__main__':    
    op = raw_input('''
input your operating character:
(E)xport, export data to ini file to translate.
(I)mport, import data from ini file translate completely.
''')
    if op.lower() == 'i' or op.lower() == 'import':
        importData()
    else:
        exportData()
