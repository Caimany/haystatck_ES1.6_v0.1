# -*- coding: UTF-8 -*-import sys,jsonimport jsonimport urllib2import requests,pycurlimport simplejsondef elastic_token(url,data):    strtoken=requests.post(url, data).content    dic_strtoken=json.loads(strtoken)    list_strtoken = dic_strtoken["tokens"]    list_len=len(list_strtoken)    print(list_len)    strtoken_all=''    for i in range(list_len):        dic=list_strtoken[i]        print dic["token"]        strtoken_all=dic["token"]+' '+strtoken_all    return strtoken_all.rstrip()# print elastic_token("http://localhost:9200/haystack_fzw/_analyze?tokenizer=ik","德国慕尼黑")### print type( dic_strtoken["tokens"] )#