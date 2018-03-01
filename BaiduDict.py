# -*- coding: utf-8 -*-

import wx
import json
import threading
import time
import Queue
import urllib2
import sqlite3
import requests
import datetime
import re
import wx.html2
from bs4 import BeautifulSoup
import os

from hashlib import md5
from urllib import quote

try:
    import httplib
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
except ImportError:
    import http.client as httplib
import random

appid = ''
secretKey = ''

langList = ['zh', 'en', 'yue', 'wyw', 'jp', 'kor', 'fra', 'spa', 'th', 'ara', 'ru', 'pt',
            'de', 'it', 'el', 'nl', 'pl', 'bul','est', 'dan', 'fin', 'cs', 'rom',
            'slo', 'swe', 'hu', 'cht', 'vie']

errReason = {u'52002': u'系统错误， 请重试', u'52001': u'请求超时，请重试', u'52003': u'未授权用户，请检查appid是否正确，或者服务是否开通',
             u'54000':u'必填参数为空，请检查参数', u'54001':u'签名错误，请检查签名生成方法', u'54003' : u'访问频率受限，请检查您的调用频率',
             u'54004':u'账户余额不足，请充值', u'54005':u'长query请求频繁，请求降低长query的发送频率，3s后再试',
             u'58000':u'客户端IP非法，请检查个人资料里的IP是否正确', u'58001':u'译文语言方向不支持, 检查译文语言是否在语言列表中'}

langType = [u'中文', u'英文']
langValue = {u'中文' : 'zh', u'英文' : 'en'}
exit_flag = False
threads_list = []
log_file = "./BaiduDictLog.txt"
photo_path = "D:/Code/BaiduDict/resource/Daily/"
picture_url = "http://cdn.iciba.com/news/word/"
text_url = "http://sentence.iciba.com/index.php?callback=jQuery19006800050563974303_1517927373529&c=dailysentence&m=getdetail&title="
url = "http://dict.cn/"

cur_picture_name = ""
cur_text = []
#basic_ul = []
shape = []
detail = []
sort = []
phrase = []
ess = []
discrim = []

work_type_list = ['translate', 'query', 'quit', 'copytrans', 'clear']
log_work_empty_cond = threading.Condition()
log_work_queue = Queue.Queue(0)

def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def init_worker(work_type, work_data):
    global  log_work_empty_cond
    tempworker = worker(work_type, work_data)
    log_work_empty_cond.acquire()
    if log_work_queue.empty():
        log_work_queue.put(tempworker)
        log_work_empty_cond.notify()
    else:
        log_work_queue.put(tempworker)
    log_work_empty_cond.release()

def obtain_picture():
    global cur_picture_name
    today = datetime.date.today()
    time_format = today.strftime("%Y-%m-%d")
    conn = sqlite3.connect("BaiduDictV1.db")
    c = conn.cursor()
    sql_query = "select PHOTO_NAME from Daily where DATE_TIME = " + '"' + time_format + '";'
    c.execute(sql_query)
    result_list = c.fetchall()
    if len(result_list) == 0:
        time_format = today.strftime("%Y%m%d")
        new_file_name = "big_" + time_format + "b.jpg"
        new_url = picture_url + new_file_name
        try:
            file_full_path = r"D:/Code/BaiduDict/resource/Daily/" + new_file_name
            respone = urllib2.urlopen(new_url)
            f = open(file_full_path, "wb")
            f.write(respone.read())
            f.close()
            cur_picture_name = new_file_name
        except urllib2.URLError as e:
            print e.reason
            sql_query = "select PHOTO_NAME from Daily order by random() limit 1;"
            c.execute(sql_query)
            result_list = c.fetchall()
            cur_picture_name = result_list[0][0]
    else:
        cur_picture_name = result_list[0][0]
    conn.close()

def obtain_text():
    today = datetime.date.today()
    time_format = today.strftime("%Y-%m-%d")
    time_format2 = today.strftime("%Y%m%d")
    conn = sqlite3.connect("BaiduDictV1.db")
    c = conn.cursor()
    sql_query = "select SOURCE_SENTENCE, TRANSLATION_SENTENCE from Daily where DATE_TIME = " + '"' + time_format + '";'
    c.execute(sql_query)
    result_list = c.fetchall()
    if len(result_list) == 0:
        newurl = text_url + time_format
        r = requests.get(newurl)
        result = re.findall(r'{.*}', r.text)[0]
        value = json.loads(result)
        source_sentence = value['content'].replace('"', "''")
        translation_sentence = value['note'].replace('"', "''")
        note = value['translation'].replace('"', "''")
        photo_name = "big_" + time_format2 + "b.jpg"
        sql_query = "insert into Daily(ID, DATE_TIME, SOURCE_SENTENCE, TRANSLATION_SENTENCE, NOTE, PHOTO_NAME) values(" + '''NULL''' + ''',"''' + time_format + '''", "''' + source_sentence + '''", "''' + translation_sentence + '''", "''' + note + '''", "''' + photo_name + '''");'''
        c.execute(sql_query)
        conn.commit()
        cur_text.append(value['content'])
        print value['content']
        cur_text.append(value['note'])
        print value['note']
    else:
        print result_list[0][0], result_list[0][1]
        cur_text.append(result_list[0][0])
        cur_text.append(result_list[0][1])
    conn.close()

class worker:
    def __init__(self, work_type, work_data):
        self.work_type = work_type
        self.work_data = work_data

    def get_type(self):
        return self.work_type

    def get_data(self):
        return self.work_data

class Crawler:
    def __init__(self, url):
        self.url = url
        try:
            self.respone = urllib2.urlopen(self.url)
            self.soup = BeautifulSoup(self.respone, "html.parser")
        except urllib2.HTTPError as e:
            print e.reason
            html_fd = open(r"D:/Code/BaiduDict/resource/HTML/default.html")
            html_doc = html_fd.read()
            self.soup = BeautifulSoup(html_doc, "html.parser")
        except urllib2.URLError as e:
            print e.reason
            html_fd = open(self.url)
            html_doc = html_fd.read()
            self.soup = BeautifulSoup(html_doc, "html.parser")

    def grab_basic_ul(self, basic_ul):
        shape_list = []
        meaning = []
        clearfix_tag = self.soup.find('div', class_ = "basic clearfix")
        if clearfix_tag is None:
            return -1
        basic_ul_tag = clearfix_tag.find('ul', class_ = "dict-basic-ul")
        span_tags = basic_ul_tag.find_all('span')
        for span_tag in span_tags:
            shape_list.append(span_tag.text.strip())
        strong_tags = basic_ul_tag.find_all('strong')
        for strong_tag in strong_tags:
            meaning.append(strong_tag.text.strip())
        basic_ul.append(shape_list)
        basic_ul.append(meaning)

        for i in range(0, len(basic_ul[0])):
            print basic_ul[0][i], basic_ul[1][i]

        return 0

    def grab_shape(self):
        label_list = []
        word_list = []
        shape_tag = self.soup.find('div', class_ = "shape")
        label_tags = shape_tag.find_all('label')
        for label_tag in label_tags:
            label_list.append(label_tag.text.strip())
        a_tags = shape_tag.find_all('a')
        for a_tag in a_tags:
            word_list.append(a_tag.text.strip())
        shape.append(label_list)
        shape.append(word_list)

        if len(shape) != 0:
            for i in range(0, len(shape[0])):
                print shape[0][i], shape[1][i]
        else:
            print "no shape information"

    def grab_detail(self):
        span_list = []
        bdo_list = []
        detail_list = []
        num_list = []
        i = 0
        detail_tag = self.soup.find('div', class_ = 'layout detail')
        span_tags = detail_tag.find_all('span')
        for span_tag in span_tags:
            next = span_tag.next_element
            span_list.append(next.strip())
            bdo_tag = span_tag.find('bdo')
            bdo_list.append(bdo_tag.text.strip())
        ol_tags = detail_tag.find_all('ol')
        for ol_tag in ol_tags:
            li_tags = ol_tag.find_all('li')
            for li_tag in li_tags:
                detail_list.append(li_tag.text.strip())
                i += 1
            num_list.append(i)

        detail.append(span_list)
        detail.append(bdo_list)
        detail.append(detail_list)
        detail.append(num_list)

        k = 0
        if len(detail) > 0:
            for i in range(0, len(detail[0])):
                print detail[0][i], detail[1][i]
                for j in range(k, detail[3][i]):
                    print detail[2][j]
                    k = detail[3][i]

    def grab_sort(self):
        i = 0
        shape_list = []
        example_list = []
        num_list = []
        sort_tag = self.soup.find('div', class_ = "layout sort")
        type_tags = sort_tag.find_all("b")
        for type_tag in type_tags:
            shape_list.append(re.sub('[\r\n\t]', '', type_tag.text))

        ol_tags = sort_tag.find_all("ol")
        for ol_tag in ol_tags:
            li_tags = ol_tag.find_all("li")
            for li_tag in li_tags:
                example_list.append(li_tag.text.strip())
                i += 1
            num_list.append(i)

        sort.append(shape_list)
        sort.append(example_list)
        sort.append(num_list)

        print sort
        k = 0
        for i in range(0, len(sort[0])):
            print sort[0][i]
            for j in range(k, sort[2][i]):
                print sort[1][j]
                k = sort[2][i]

    def grab_phrase(self):
        shape_list = []
        type_list = []
        example_list = []
        phrase_tag = self.soup.find('div', class_ = "layout phrase")
        type_tags = phrase_tag.find_all('b')
        for type_tag in type_tags:
            shape_list.append(re.sub('[\r\t\n]', '', type_tag.text))
        dl_tags = phrase_tag.find_all('dl')
        for dl_tag in dl_tags:
            dt_tag = dl_tag.find('dt')
            type_list.append(dt_tag.text.strip())
            dd_tags = dl_tag.find_all('dd')
            for dd_tag in dd_tags:
                ol_tags = dd_tag.find_all("ol")
                for ol_tag in ol_tags:
                    example_list.append(re.sub('[\r\t]', '', ol_tag.text))

        phrase.append(shape_list)
        phrase.append(type_list)
        phrase.append(example_list)

        for i in range(0, len(phrase[1])):
            print phrase[1][i]
            print phrase[2][i]

    def grab_ess(self):
        shape_list = []
        bdo_list = []
        example_list = []
        num_list = []
        ess_tag = self.soup.find('div', class_ = "layout ess")
        span_tags = ess_tag.find_all('span')
        for span_tag in span_tags:
            next = span_tag.next_element
            shape_list.append(re.sub('[\r\n\t]', '', next))
            bdo_tag = span_tag.find('bdo')
            bdo_list.append(bdo_tag.text.strip())

        ol_tags = ess_tag.find_all('ol')
        i = 0
        for ol_tag in ol_tags:
            li_tags = ol_tag.find_all('li')
            for li_tag in li_tags:
                example_list.append(li_tag.text.strip())
                i += 1
            num_list.append(i)

        ess.append(shape_list)
        ess.append(bdo_list)
        ess.append(example_list)
        ess.append(num_list)

        k = 0
        for i in range(0, len(ess[0])):
            print ess[0][i], ess[1][i]
            for j in range(k, ess[3][i]):
                print ess[2][j]
            k = ess[3][i]

    def grab_discrim(self):
        shape_list = []
        bdo_list = []
        example_list = []
        title_list = []

        discrim_tag = self.soup.find('div', class_ = "layout discrim")
        span_tags = discrim_tag.find_all('span')
        for span_tag in span_tags:
            next = span_tag.next_element
            shape_list.append(re.sub('[\r\t\n]', '', next))
            bdo_tag = span_tag.find('bdo')
            bdo_list.append(bdo_tag.text)

        dl_tags = discrim_tag.find_all('dl')
        for dl_tag in dl_tags:
            dt_tag = dl_tag.find('dt')
            title_list.append(dt_tag.text.strip())
            dd_tag = dl_tag.find('dd')
            example_list.append(dd_tag.text.strip())

        discrim.append(shape_list)
        discrim.append(bdo_list)
        discrim.append(title_list)
        discrim.append(example_list)

        for i in range(0, len(discrim[2])):
            print discrim[2][i]
            print discrim[3][i]

    def gen_new_html(self):
        meta_tags = self.soup.find_all('meta')
        for meta_tag in meta_tags:
            meta_tag.extract()
        script_tags = self.soup.find_all('script')
        for script_tag in script_tags:
            script_tag.extract()

        header_tags = self.soup.find_all('div', id = "header")
        for header_tag in header_tags:
            header_tag.extract()

        footer_tags = self.soup.find_all('div', id = "footer")
        for footer_tag in footer_tags:
            footer_tag.extract()

        copyright_tags = self.soup.find_all('div', class_ = "copyright")
        for copyright_tag in copyright_tags:
            copyright_tag.extract()

        shared_tags = self.soup.find_all('div', id = "dshared")
        for shared_tag in shared_tags:
            shared_tag.extract()

        righter_tags = self.soup.find_all('div', class_ = "righter")
        for righter_tag in righter_tags:
            righter_tag.extract()

        dd_default_tags = self.soup.find_all('div', class_ = "dd_default")
        for dd_default_tag in dd_default_tags:
            dd_default_tag.extract()

        sidenav_tags = self.soup.find_all('div', class_ = "sidenav")
        for sidenav_tag in sidenav_tags:
            sidenav_tag.extract()

        head_tag = self.soup.find('head')
        new_meta_tag = self.soup.new_tag('meta', charset = "utf-8")
        head_tag.append(new_meta_tag)
        new_link_tag = self.soup.new_tag('link', rel = "stylesheet",  type = "text/css", href = "testmodule.css")
        head_tag.append(new_link_tag)

        #print self.soup.prettify()

        f = open('./resource/HTML/new.html', "w")
        f.write(self.soup.prettify().encode("utf-8"))
        f.close()

class dailySentenceMod(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        imagehbox = wx.BoxSizer(wx.HORIZONTAL)
        source_text_hbox = wx.BoxSizer(wx.HORIZONTAL)
        translation_text_hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add((-1, 15))
        obtain_picture()
        picture_path = photo_path + cur_picture_name
        print picture_path
        jpg_obj = wx.Image(picture_path, wx.BITMAP_TYPE_ANY)
        jpg_obj.Rescale(700, 435)
        bmp = jpg_obj.ConvertToBitmap()
        self.image_obj = wx.StaticBitmap(self, -1, bmp, pos= (10, 10), size = (jpg_obj.GetWidth(), jpg_obj.GetHeight()))
        imagehbox.Add(self.image_obj, flag = wx.EXPAND, border = 8)
        vbox.Add(imagehbox, flag = wx.ALIGN_CENTER)
        vbox.Add((-1, 25))

        obtain_text()
        source_text = cur_text[0]
        dest_text = self.shifter_sentence(source_text)
        self.sentence = wx.StaticText(self, -1, style = wx.ALIGN_CENTER)
        self.font = wx.Font(14, wx.ROMAN, wx.ITALIC, wx.BOLD)
        self.sentence.SetFont(self.font)
        self.sentence.SetLabel(dest_text)
        source_text_hbox.Add(self.sentence, flag = wx.ALIGN_CENTER)
        vbox.Add(source_text_hbox, flag = wx.ALIGN_CENTER)
        vbox.Add((-1, 10))

        translation_text = cur_text[1]
        self.translation = wx.StaticText(self, -1, style = wx.ALIGN_CENTER)
        self.font2 = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.translation.SetFont(self.font2)
        self.translation.SetLabel(translation_text)
        translation_text_hbox.Add(self.translation, flag = wx.EXPAND, border = 5)
        vbox.Add(translation_text_hbox, flag = wx.ALIGN_CENTER)
        vbox.Add((-1, 5))

        self.SetSizer(vbox)

    def shifter_sentence(self, source_text):
        j = 0
        source_text_list = list(source_text)
        text_len = len(source_text_list)
        for i in range(0, text_len):
            if source_text_list[i] == ',' or source_text_list[i] == ' ' or source_text_list[i] == '.':
                location = i
            if j > 92:
                source_text_list.insert(location + 1, '\n')
                j = i - location
            else:
                j += 1
        dest_text = ''.join(source_text_list)
        return dest_text

class translateMod(wx.Panel):
    def __init__(self, parent):
        panel = wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        source_select_hbox = wx.BoxSizer(wx.HORIZONTAL)
        dest_select_hbox = wx.BoxSizer(wx.HORIZONTAL)
        select_hbox = wx.BoxSizer(wx.HORIZONTAL)
        text_hbox = wx.BoxSizer(wx.HORIZONTAL)

        # self.label = wx.StaticText(panel, -1, "xxxxxx", pos = (10, 10))
        self.source_label = wx.StaticText(self, label=u'源语言')
        source_select_hbox.Add(self.source_label, flag=wx.RIGHT, border=8)
        self.source_choice = wx.Choice(self, pos=(50, 10), choices=langType)
        source_select_hbox.Add(self.source_choice, flag=wx.LEFT | wx.EXPAND, border=8)
        select_hbox.Add(source_select_hbox, proportion = 1, flag=wx.EXPAND)
        self.source_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        text_hbox.Add(self.source_text, proportion = 1, flag=wx.EXPAND)
        # wx.Button(self, u"翻译", pos = (50, 20))

        self.dest_label = wx.StaticText(self, label=u'目标语言', pos=(410, 10))
        dest_select_hbox.Add(self.dest_label, flag=wx.RIGHT, border=8)
        self.dest_choice = wx.Choice(self, pos=(460, 10), choices=langType)
        dest_select_hbox.Add(self.dest_choice, flag=wx.LEFT | wx.EXPAND, border=8)
        select_hbox.Add(dest_select_hbox, proportion = 1, flag=wx.EXPAND)
        self.dest_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        text_hbox.Add(self.dest_text, proportion = 1, flag=wx.EXPAND)
        vbox.Add(select_hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP)
        vbox.Add((-1, 10))
        vbox.Add(text_hbox, proportion = 1, flag = wx.EXPAND)
        vbox.Add((-1, 25))

        button_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.translate_button = wx.Button(self, label = u"翻译", size = (70, 30))
        button_hbox.Add(self.translate_button)
        self.clear_button = wx.Button(self, label = u"清空", size = (70, 30))
        button_hbox.Add(self.clear_button)
        self.copy_button = wx.Button(self, label = u"拷贝译文", size = (70, 30))
        button_hbox.Add(self.copy_button, flag = wx.LEFT | wx.BOTTOM, border = 5)
        vbox.Add(button_hbox, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = 10)
        self.SetSizer(vbox)

        #self.Bind(wx.EVT_TEXT_ENTER, self.translate, self.source_text)
        self.Bind(wx.EVT_BUTTON, self.translate, self.translate_button)
        #self.Bind(wx.EVT_BUTTON, self.eliminate_space, self.translate_button)
        self.Bind(wx.EVT_BUTTON, self.clear, self.clear_button)
        self.Bind(wx.EVT_BUTTON, self.copy_translation, self.copy_button)

    def eliminate_space(self):
        text = re.sub('[\r\n]', ' ', self.source_text.GetValue())
        self.source_text.SetValue(text)
        return text

    def translate(self, event):
        query = self.eliminate_space()
        print query
        myurl = '/api/trans/vip/translate'
        fromLang = langValue[self.source_choice.GetString(self.source_choice.GetCurrentSelection())]
        toLang = langValue[self.dest_choice.GetString(self.dest_choice.GetCurrentSelection())]
        salt = random.randint(32768, 65536)
        sign = appid + query + str(salt) + secretKey
        m1 = md5()
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        myurl = myurl + myurl+'?appid=' + appid + '&q=' + quote(query.encode('utf-8'))+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
        print myurl
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        res = response.read()
        content = json.loads(res)
        #print content

        try:
            translate_result = content['trans_result']
        except KeyError:
            code = content['error_code']
            print errReason[code]
            init_worker('error', '' + errReason[code])
            return

        if translate_result != 'None':
            print translate_result
            for i in range(0, len(translate_result)):
                print('\033[1;31m# \033[0m %s %s' % ((translate_result[i]['src']), (translate_result[i]['dst'])))
                self.dest_text.SetValue(translate_result[i]['dst'])
                init_worker('translate', '' + translate_result[i]['src'] + ":" + translate_result[i]['dst'])

    def clear(self, event):
        self.source_text.Clear()
        self.dest_text.Clear()
        init_worker('clear', 'clear source and dest window')

    def copy_translation(self, event):
        text_obj = wx.TextDataObject()
        wx.TheClipboard.Open()
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            text_obj.SetText(self.dest_text.GetValue())
            wx.TheClipboard.SetData(text_obj)
            wx.TheClipboard.Close()
        init_worker('copytrans', self.dest_text.GetValue())

class dictMod(wx.Panel):
    def __init__(self, parent):
        panel = wx.Panel.__init__(self, parent)
        vbox_sizer = wx.BoxSizer(wx.VERTICAL)
        search_hbox = wx.BoxSizer(wx.HORIZONTAL)
        web_hbox = wx.BoxSizer(wx.HORIZONTAL)
        input_hbox = wx.BoxSizer(wx.HORIZONTAL)
        button_hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox_sizer.Add((-1, 10))
        #input_hbox.Add((20, -1))
        self.input = wx.TextCtrl(self, size = (400, 30))
        input_hbox.Add(self.input, flag=wx.CENTER)
        button_img = wx.Bitmap("./resource/System/query_button.ico", wx.BITMAP_TYPE_ICO)
        self.search_button = wx.BitmapButton(self, id=wx.ID_ANY, bitmap=button_img, size=(70, 30))
        input_hbox.Add(self.search_button, flag = wx.CENTER)
        vbox_sizer.Add(input_hbox)
        vbox_sizer.Add((-1, 10))
        self.browser = wx.html2.WebView.New(self, url=r"D:/Code/BaiduDict/resource/HTML/testsoup.html",
                                            size=(850, 500))
        web_hbox.Add(self.browser, flag=wx.EXPAND)
        vbox_sizer.Add(web_hbox, flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(vbox_sizer)

        self.Bind(wx.EVT_TEXT_ENTER, self.search, self.input)
        self.Bind(wx.EVT_BUTTON, self.search, self.search_button)
        self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.relation_query, self.browser)

    def relation_query(self, event):
        new_url = event.GetURL()
        if new_url[0] != 'D' and new_url[0] != 'd':
            crawler_newer = Crawler(new_url)
            crawler_newer.gen_new_html()
            self.browser.LoadURL(r"D:/Code/BaiduDict/resource/HTML/new.html")

    def search(self, event):
        global url
        word = self.input.GetValue()
        if len(word) == 0:
            dial = wx.MessageDialog(None, u"请输入有效的单词", "Warning", wx.YES_NO | wx.ICON_WARNING)
            ret = dial.ShowModal()
            if ret == wx.ID_YES:
                pass
        else:
            new_url = url + word
            print new_url
            if new_url[0] != 'D' and new_url[0] != 'd':
                crawler_newer = Crawler(new_url)
                crawler_newer.gen_new_html()
                self.browser.LoadURL(r"D:/Code/BaiduDict/resource/HTML/new.html")
                if check_contain_chinese(word) is False:
                    basic_ul = []
                    if crawler_newer.grab_basic_ul(basic_ul) != 0:
                        init_worker('warning', "this word %s is an invalid word" % (word))
                    else:
                        basic_ul.append(word)
                        init_worker('dict', basic_ul)

class learnMod(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, label = "Page Three")

class logThread(threading.Thread):
    def __init__(self, thread_id, thread_name, work_queue):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.work_queue = work_queue
        try:
            self.log_file = open(log_file, "a")
        except IOError as err:
            print "File Error: " + str(err)

    def run(self):
        global exit_flag, log_work_empty_cond
        print "Starting " + self.name
        while True:
            if log_work_empty_cond.acquire():
                if self.work_queue.empty():
                    log_work_empty_cond.wait()
                else:
                    tempworker = self.work_queue.get()
                    self.process_work(tempworker)
                    if exit_flag == True:
                        log_work_empty_cond.release()
                        break
                log_work_empty_cond.release()
        self.log_file.close()

    def process_work(self, worker):
        global exit_flag
        work_type = worker.work_type
        work_data = worker.work_data
        if work_type == 'quit':
            exit_flag = True
            self.log_file.write("[%s][%s]\n" %(time.ctime(time.time()), work_type))
        elif work_type == 'dict':
            word = work_data.pop()
            word_meaing = ''
            for i in range(0, len(work_data[0])):
                word_meaing = word_meaing + work_data[0][i] + work_data[1][i]
            conn = sqlite3.connect("BaiduDictV1.db")
            c = conn.cursor()
            sql_str = 'select WORD from WORDS where WORD = "' + word + '";'
            c.execute(sql_str)
            result_list = c.fetchall()
            if len(result_list) == 0:
                sql_str = 'insert into WORDS(WORD, MEANING, FRENQUENCE) values(' + '"' + word + '", "' + word_meaing + '", ' + '1);'
                c.execute(sql_str)
                conn.commit()
            else:
                sql_str = 'update WORDS set FRENQUENCE = (FRENQUENCE + 1) where WORD = "' + word + '";'
                c.execute(sql_str)
                conn.commit()
            conn.close()
        else:
            self.log_file.write("[%s][%s][%s]\n" % (time.ctime(time.time()), work_type, work_data))

    def print_time(self):
        time.sleep(2)
        print "%s:%s" % (self.thread_name, time.ctime(time.time()))
        self.log_file.write("%s:%s\n" % (self.thread_name, time.ctime(time.time())))

class myFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent = parent, title = title, size = (850, 600), style = wx.DEFAULT_FRAME_STYLE & (~wx.RESIZE_BORDER))
        icon = wx.Icon()
        icon.LoadFile("BaiduDict.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.Bind(wx.EVT_CLOSE, self.closeWindow)

    def closeWindow(self, event):
        dial = wx.MessageDialog(None, u"确定退出BaiduDict吗？", "Question", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            global exit_flag
            init_worker('quit', '')
            for threadobj in threads_list:
                threadobj.join()
            self.Destroy()
        else:
            event.Veto()

if __name__ == "__main__":
    thread1 = logThread(1, "Thread-1", log_work_queue)
    thread1.start()
    threads_list.append(thread1)
    app = wx.App()
    frame = myFrame(None, "BaiduDict")
    nb = wx.Notebook(frame, style = wx.NB_LEFT)
    nb.AddPage(dailySentenceMod(nb), "每日一句")
    nb.AddPage(translateMod(nb), "翻译")
    nb.AddPage(dictMod(nb), "词典")
    nb.AddPage(learnMod(nb), "单词学习")
    frame.Show(True)
    app.MainLoop()
