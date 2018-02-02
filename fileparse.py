#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3

fileName = u'./GRE.txt'
flag = True
location = 0
wordList = []
bar = "[>                                                 ]"

try:
    fObj = open(fileName, 'r')
except IOError as e:
    print "open file--", fileName, "--error: ", e
    exit(-1)

wordTup = []
word = ''
meaning = ''

for eachline in fObj:
    #print eachline
    wordDict = {}
    if flag == True:
        for letter in eachline.decode('utf-8'):
            if letter != '\n':
                word += letter.encode('utf-8')
        #print word
        flag = False
    else:
        for letter in eachline.decode('utf-8'):
            if letter != '\n':
                meaning += letter.encode('utf-8')
        #print meaning
        wordDict[word] = meaning
        wordList.append(wordDict)
        word = ''
        meaning = ''
        flag = True

#print len(wordList)
#i = 0
#for text in wordList:
#    if i == 10:
#        break
#    for key in text:
#        print text[key].decode('utf-8')
#    i += 1
#print '........................'
#for text in wordList:
#    for key in text:
#        if key == "abash":
#            print  text[key].decode('utf-8')

conn = sqlite3.connect("GRE.db")
print "open database successfully"
c = conn.cursor()

c.execute('''create table WORDSENSE(
          word char(50) PRIMARY KEY NOT NULL,
           meaning char(50) NOT NULL);''')
print "table WORD create successfully"

x = 0
i = 0

barList = list(bar)
print '\r' + bar,
for text in wordList:
    for key in text:
        if x < i / 150:
            x = i / 150
            barList[x] = '='
            if x != 49:
                barList[x + 1] = '>'
            bar = ''.join(barList)
            print '\r' + "complete (%d/%d): " % (i, len(wordList)) + bar,
        else:
            print '\r' + "complete (%d/%d): " % (i, len(wordList)) + bar,

        sqlStr = "insert into GREWORD(word, meaning) VALUES(" + "'" + key + "', '" + text[key] + "');"
        c.execute(sqlStr)
        conn.commit()
        i += 1

cursor = c.execute("select * from GREWORD where word = 'abash';")
for row in cursor:
    print row[0], row[1]

fObj.close()
conn.close()