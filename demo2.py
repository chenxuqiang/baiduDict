#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import wx
from hashlib import md5
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
import sys
try:
    import httplib
    import sys  
    reload(sys)  
    sys.setdefaultencoding('utf8')
except ImportError:
    import http.client as httplib
import random

appid = 'xxxxxxxxxxxxxxxxx'
secretKey = 'xxxxxxxxxxxxxx'
langList = ['zh', 'en', 'yue', 'wyw', 'jp', 'kor', 'fra', 'spa', 'th', 'ara', 'ru', 'pt',
            'de', 'it', 'el', 'nl', 'pl', 'bul','est', 'dan', 'fin', 'cs', 'rom',
            'slo', 'swe', 'hu', 'cht', 'vie']
errReason = {u'52001':u'请求超时，请重试', u'52002':u'系统错误， 请重试', u'52003':u'未授权用户，请检查appid是否正确，或者服务是否开通',
             u'54000':u'必填参数为空，请检查参数', u'54001':u'签名错误，请检查签名生成方法', u'54003' : u'访问频率受限，请检查您的调用频率',
             u'54004':u'账户余额不足，请充值', u'54005':u'长query请求频繁，请求降低长query的发送频率，3s后再试',
             u'58000':u'客户端IP非法，请检查个人资料里的IP是否正确', u'58001':u'译文语言方向不支持, 检查译文语言是否在语言列表中'}

class DictUI(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (800, 600))
        panel = wx.Panel(self, -1)
        self.transButton = wx.Button(panel, -1, u"翻译", pos=(10, 250))
        self.Bind(wx.EVT_BUTTON, self.Translate, self.transButton)
        self.transButton.SetDefault()
        self.cleanButton = wx.Button(panel, -1, u'清空', pos = (110, 250))
        self.Bind(wx.EVT_BUTTON, self.Clean, self.cleanButton)
        self.cleanButton.SetDefault()
        self.control1 = wx.TextCtrl(panel, style=wx.TE_MULTILINE, pos=(10, 10), size = (700, 200))
        self.control2 = wx.TextCtrl(panel, style = wx.TE_MULTILINE, pos = (10, 300), size = (700, 200))
        self.fromLangLabel = wx.StaticText(panel, -1, u"源语言", pos = (720, 10))
        self.fromLangChoice = wx.Choice(panel, -1, pos=(720, 50), choices = langList)
        self.toLangLabel = wx.StaticText(panel, -1, u"目标语言", pos = (720, 300))
        self.toLangChoice = wx.Choice(panel, -1, pos = (720, 350), choices = langList)
        self.Show(True)

        self.CreateStatusBar()

    def Clean(self, event):
        self.control2.Clear()
        self.control1.Clear()

    def Translate(self, event):
        q = self.control1.GetValue()
        print q
        myurl = '/api/trans/vip/translate'
        fromLang = langList[self.fromLangChoice.GetSelection()]
        toLang = langList[self.toLangChoice.GetSelection()]
        content = None
        httpClient = None
        salt = random.randint(32768, 65536)
        sign = appid + q + str(salt) + secretKey
        m1 = md5()
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        myurl = myurl + myurl+'?appid=' + appid + '&q=' + quote(q.encode('utf-8'))+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
        print myurl
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        res = response.read()
        content = json.loads(res)
        print content
        try:
            translate_result = content['trans_result']
        except KeyError:
            code = content['error_code']
            print errReason[code]
            return

        if translate_result != 'None':
            print translate_result
            for i in range(0, len(translate_result)):
                print('\033[1;31m# \033[0m %s %s' % ((translate_result[i]['src']), (translate_result[i]['dst'])))
                self.control2.SetValue(translate_result[i]['dst'])

if __name__ == '__main__':
    app = wx.App(False)
    frame = DictUI(None, "BaiduDict")
    app.MainLoop()
