# -*- coding: utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup

meaning = []
shape = []
detail = []
dual = []
en_meaning = []
sort = []
patt = []
phrase = []
coll = []
ess = []
discrim = []
nfo = []
derive = []
nwd = []

def get_meaning_list():
    items = soup.find_all("div", class_ = "basic clearfix")
    for item in items:
        chinese_meaning = []
        part_of_speech = []
        strong_tag = item.find_all('strong')
        for strong_text in strong_tag:
            #print strong_text.text
            chinese_meaning.append(strong_text.text)
        meaning.append(chinese_meaning)
        span_tag = item.find_all('span')
        for span_text in span_tag:
            #print span_text.text
            part_of_speech.append(span_text.text)
        meaning.append(part_of_speech)

    for i in range (0, len(meaning[0])):
        for j in range(len(meaning), 0, -1):
            print meaning[j - 1][i],
        print ''


def get_shape_list():
    items = soup.find_all("div", class_ = "shape")
    for item in items:
        chinese_shape = []
        english_word = []
        label_tag = item.find_all('label')
        for label_text in label_tag:
           # print label_text.text.strip()
            chinese_shape.append(label_text.text.strip())
        shape.append(chinese_shape)
        word_tag = item.find_all('a')
        for word_text in word_tag:
            #print word_text.text.strip()
            english_word.append(word_text.text.strip())
        shape.append(english_word)

    for i in range(0, len(shape[0])):
        for j in range(0, len(shape)):
            print shape[j][i],
        print ''

def get_detail_list():
    detail_layout_tag = soup.find_all("div", class_ = "layout detail")
    for item in detail_layout_tag:
        word_shape = []
        detail_meaning = []
        bdo_tag = item.find_all("bdo")
        for bdo_text in bdo_tag:
            word_shape.append(bdo_text.text.strip())
        detail.append(word_shape)
        ol_tags = item.find_all('ol')
        for ol_tag in ol_tags:
            li_tags = ol_tag.find_all('li')
            li_list = []
            for li_tag in li_tags:
                li_list.append(li_tag.text.strip())
            detail_meaning.append(li_list)
        detail.append(detail_meaning)

    for i in range(0, len(detail[0])):
        print detail[0][i], ":",
        for j in range(0, len(detail[1][i])):
            print detail[1][i][j], '、',
        print ''

def get_dual_list():
    dual_tag = soup.find_all("div", class_ = "layout dual")
    for item in dual_tag:
        word_shape = []
        dual_meaning = []
        bdo_tag = item.find_all("bdo")
        for bdo_text in bdo_tag:
            word_shape.append(bdo_text.text.strip())
        dual.append(word_shape)
        ol_tags = item.find_all('ol')
        for ol_tag in ol_tags:
            ol_list = []
            li_tags = ol_tag.find_all('li')
            for li_tag in li_tags:
                li_list = []
                strong_tags = li_tag.find_all('strong')
                for strong_tag in strong_tags:
                    li_list.append(strong_tag.text.strip())
                li_list.append(li_tag.text.strip())
                ol_list.append(li_list)
            dual_meaning.append(ol_list)
        dual.append(dual_meaning)

    for i in range(0, len(dual[0])):
        print dual[0][i], " ",
        for j in range(0, len(dual[1][i])):
            print dual[1][i][j][0], dual[1][i][j][1],
        print ' '

def get_en_list():
    en_tags = soup.find_all('div', class_ = "layout en")
    for en_tag in en_tags:
        word_shape = []
        en = []
        span_tags = en_tag.find_all("span")
        for span_tag in span_tags:
            word_shape.append(span_tag.text.strip())
        en_meaning.append(word_shape)
        ol_tags = en_tag.find_all("ol")
        for ol_tag in ol_tags:
            templist = []
            li_tags = ol_tag.find_all("li")
            for li_tag in li_tags:
                templist.append(li_tag.text)
            en.append(templist)
        en_meaning.append(en)

    for i in range(0, len(en_meaning[0])):
        print en_meaning[0][i],
        for j in range(0, len(en_meaning[1][i])):
            print en_meaning[1][i][j],
        print ''

def get_sort_list():
    sort_tags = soup.find_all('div', class_ = "layout sort")
    for sort_tag in sort_tags:
        word_shape = []
        example = []
        type_tags = sort_tag.find_all("b")
        for type_tag in type_tags:
            word_shape.append(type_tag.text.strip())
        sort.append(word_shape)

        ol_tags = sort_tag.find_all("ol")
        for ol_tag in ol_tags:
            templist = []
            li_tags = ol_tag.find_all("li")
            for li_tag in li_tags:
                templist.append(li_tag.text.strip())
            example.append(templist)
        sort.append(example)

    for i in range(0, len(sort[0])):
        print sort[0][i],
        for j in range(0, len(sort[1][i])):
            print sort[1][i][j],
        print ' '

def get_patt_list():
    patt_tags = soup.find_all('div', class_ = "layout patt")
    for patt_tag in patt_tags:
        word_shape = []
        pattern = []
        type_divs = patt_tag.find_all("div")
        for type_div in type_divs:
            word_shape.append(type_div.text.strip())
        patt.append(word_shape)

        ol_tags = patt_tag.find_all("ol")
        for ol_tag in ol_tags:
            templist = []
            li_tags = ol_tag.find_all("li")
            for li_tag in li_tags:
                templist.append(li_tag.text.strip())
            pattern.append(templist)
        patt.append(pattern)
    for i in range(0, len(patt[0])):
        print patt[0][i],
        for j in range(0, len(patt[1][i])):
            print patt[1][i][j],
        print ''

def get_phrase_list():
    phrase_tags = soup.find_all('div', class_ = "layout phrase")
    for phrase_tag in phrase_tags:
        word_shape = []
        word_phrase = []
        example = []
        type_divs = phrase_tag.find_all('div')
        for type_div in type_divs:
            word_shape.append(type_div.text.strip())
        phrase.append(word_shape)

        dl_tags = phrase_tag.find_all("dl")
        for dl_tag in dl_tags:
            dt_tags = dl_tag.find_all("dt")
            for dt_tag in dt_tags:
                word_phrase.append(dt_tag.text.strip())
            dd_tags = dl_tag.find_all("dd")
            for dd_tag in dd_tags:
                example.append(dd_tag.text.strip())
        phrase.append(word_phrase)
        phrase.append(example)

    for i in range(0, len(phrase[1])):
        print phrase[1][i]
        print phrase[2][i]
        print "..............................................."

def get_coll_list():
    coll_tags = soup.find_all("div", class_ = "layout coll")
    for coll_tag in coll_tags:
        div_list = []
        b_list = []
        word_shape = []
        collocation = []
        div_tags = coll_tag.find_all('div')
        for div_tag in div_tags:
            div_list.append(div_tag.text.strip())
        b_tags = coll_tag.find_all('b')
        for b_tag in b_tags:
            b_list.append(b_tag.text.strip())
        for item in b_list:
            if item not in div_list:
                word_shape.append(item)
        coll.append(word_shape)

        ul_tags = coll_tag.find_all('ul')
        for ul_tag in ul_tags:
            #collocation.append(ul_tag.text.replace('\t', ''))
            collocation.append(re.sub('[\r\t]', '', ul_tag.text))
        coll.append(collocation)

    print coll[1]
    for i in range(0, len(coll[0])):
        print coll[0][i]
        print coll[1][i]

def get_ess_list():
    ess_tag = soup.find('div', class_ = "layout ess")
    word_shape = []
    usage = []
    bdo_tags = ess_tag.find_all("bdo")
    for bdo_tag in bdo_tags:
        word_shape.append(bdo_tag.text.strip())
    ess.append(word_shape)

    ol_tags = ess_tag.find_all("ol")
    for ol_tag in ol_tags:
        usage.append(re.sub('[\r\t\n]', '', ol_tag.text))
    ess.append(usage)

    for i in range(0, len(ess[0])):
        print ess[0][i]
        print ess[1][i]

def get_discrim_list():
    discrim_tag = soup.find('div', class_ = "layout discrim")
    word_shape = []
    discrimination = []
    templist = []
    bdo_tags = discrim_tag.find_all('bdo')
    for bdo_tag in bdo_tags:
        word_shape.append(bdo_tag.text.strip())
    discrim.append(word_shape)

    dt_tags = discrim_tag.find_all("dt", class_ = "on")
    for dt_tag in dt_tags:
        templist.append(dt_tag.text.strip())
    discrim.append(templist)

    dd_tags = discrim_tag.find_all("dd")
    for dd_tag in dd_tags:
        discrimination.append(re.sub('[\r\t\n]', '', dd_tag.text))
    discrim.append(discrimination)

    for i in range(0, len(discrim[1])):
        print discrim[1][i], ":", discrim[2][i]

def get_nfo_list():
    nfo_tag = soup.find("div", class_ = "layout nfo")
    type_list = []
    word_example = []
    type_divs = nfo_tag.find_all('div')
    for type_div in type_divs:
        type_list.append(type_div.text.strip())
    nfo.append(type_list)

    ul_tags = nfo_tag.find_all('ul')
    for ul_tag in ul_tags:
        word_example.append(re.sub('[\r\t\n]', '', ul_tag.text))
    nfo.append(word_example)

    for i in range(0, len(nfo[0])):
        print nfo[0][i], ":", nfo[1][i]

def get_derive_list():
    derive_tag = soup.find("div", class_ = "layout derive")
    ul_tags = derive_tag.find_all('ul', slider =  "5")
    for ul_tag in ul_tags:
        derive.append(re.sub('[\r\t\n]', ' ', ul_tag.text))

    for i in range(0, len(derive)):
        print derive[i]

def get_nwd_list():
    nwd_tag = soup.find("div", class_ = "layout nwd")
    a_tags = nwd_tag.find_all("a")
    for a_tag in a_tags:
        nwd.append(re.sub('[\r\t\n]', '', a_tag.text))

    for i in range(0, len(nwd)):
        print nwd[i],

if __name__ == "__main__":
    url = "http://dict.cn/water"
    response = urllib2.urlopen(url)
    soup = BeautifulSoup(response, "html.parser")
    #get_meaning_list()
    #get_shape_list()
    #get_detail_list()
    #get_dual_list()
    #get_en_list()
    #get_sort_list()
    #get_patt_list()
    #get_phrase_list()
    #get_coll_list()
    #get_ess_list()
    #get_discrim_list()
    #get_nfo_list()
    #get_derive_list()
    #get_nwd_list()

