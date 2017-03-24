__author__ = 'caimujia@foxmail.com'
# -*- coding: utf-8 -*-
from django import forms
from haystack.forms import FacetedSearchForm, HighlightedSearchForm, SearchForm
from haystack.query import SQ

import pytz

from django.utils import timezone


"""
# 分词查询
"""
import urllib2, json

analyze_url = 'http://172.18.9.65:9200/_analyze'


class SearchForm_gdftu(FacetedSearchForm, HighlightedSearchForm):
    order_by_time = forms.IntegerField(required=False)
    start_applytime = forms.CharField(required=False)
    end_applytime = forms.CharField(required=False)
    autolink = forms.CharField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SearchForm_gdftu, self).search()
        # sqs = self.searchqueryset.filter_and(SQ(title=self.cleaned_data['q']) | SQ(content=self.cleaned_data['q']))

        # print "处理前",sqs.count()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['order_by_time'] == 1:
            sqs = sqs.filter_and(webid='3').order_by('-textdate')
        else:
            sqs = sqs.filter_and(webid='3').order_by('-_score')

        # if self.cleaned_data['autolink'] :
        #     sqs = sqs.filter_and(autolink=self.cleaned_data['autolink'])

        # Check to see if a start_date was chosen.
        if sqs.count() == 0:
            pass
        else:
            if self.cleaned_data['start_applytime'] and self.cleaned_data['end_applytime']:
                sqs = sqs.filter_and(textdate__gte=self.cleaned_data['start_applytime'], \
                                     textdate__lte=self.cleaned_data['end_applytime'])
        return sqs


class SearchForm_pprd(FacetedSearchForm, HighlightedSearchForm):
    order_by_time = forms.IntegerField(required=False)
    start_applytime = forms.CharField(required=False)
    end_applytime = forms.CharField(required=False)
    item = forms.CharField(required=False)

    ## item对应关系 :
    # pprd_item_dic={
    # 'news':'wx','message':'xx',\
    # 'gd':'guangdong','ac':'ac'
    # }


    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SearchForm_pprd, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['order_by_time'] == 1:
            sqs = sqs.filter_and(webid='1').order_by('-textdate')
        else:
            sqs = sqs.filter_and(webid='1').order_by('-_score')

        if self.cleaned_data['item'] == 1:
            #
            pass

        # if self.cleaned_data['autolink'] :
        #     sqs = sqs.filter_and(autolink=self.cleaned_data['autolink'])
        # Check to see if a start_date was chosen.
        if sqs.count() == 0:
            pass
        else:
            if self.cleaned_data['start_applytime'] and self.cleaned_data['end_applytime']:
                sqs = sqs.filter_and(textdate__gte=self.cleaned_data['start_applytime'], \
                                     textdate__lte=self.cleaned_data['end_applytime'])

        return sqs


class SearchForm_gd(HighlightedSearchForm):
    order_by_time = forms.IntegerField(required=False)
    start_applytime = forms.CharField(required=False)
    end_applytime = forms.CharField(required=False)
    autolink = forms.CharField(required=False)

    # 不包含关键字
    exclude = forms.CharField(required=False)
    texclude = forms.CharField(required=False)
    cexclude = forms.CharField(required=False)

    # 搜索位置
    stitle = forms.CharField(required=False)
    scontent = forms.CharField(required=False)

    def query_ansj_token(self, text=""):
        url = analyze_url
        data = {}
        data['analyzer'] = 'query_ansj'
        data['text'] = text
        # print text.__class__,text
        # url_values = urllib.urlencode(data)
        # full_url = url + '?' + url_values
        #
        # jresponse = json.load( urllib2.urlopen(full_url))
        str_text = ""
        data = json.dumps(data)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        jresponse = eval(f.read())

        for i in jresponse['tokens']:
            str_text = str_text + i['token'] + ' '

        # 格式化搜索关键字
        return str_text.rstrip()

    def unicode_ansj(self, data):
        # return unicode(self.query_ansj_token(data), "UTF-8")
        return data

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = self.searchqueryset

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['order_by_time'] == 1:
            sqs = sqs.filter_and(webid='11').order_by('-textdate')
        else:
            sqs = sqs.filter_and(webid='11').order_by('-_score', '-textdate')

        # Check to see if a start_date was chosen.
        if sqs.count() == 0:
            pass
        else:
            if self.cleaned_data['start_applytime'] and self.cleaned_data['end_applytime']:
                sqs = sqs.filter_and(textdate__gte=self.cleaned_data['start_applytime'],
                                     textdate__lte=self.cleaned_data['end_applytime'])

            ###
            if self.cleaned_data['exclude']:
                sqs = sqs.exclude(text=self.unicode_ansj(self.cleaned_data['exclude']))
            if self.cleaned_data['texclude']:
                sqs = sqs.exclude(title=self.unicode_ansj(self.cleaned_data['texclude']))
            if self.cleaned_data['cexclude']:
                sqs = sqs.exclude(content=self.unicode_ansj(self.cleaned_data['cexclude']))

            if self.cleaned_data['stitle']:
                sqs = sqs.filter_and(title=self.unicode_ansj(self.cleaned_data['stitle']))
            elif self.cleaned_data['scontent']:
                sqs = sqs.filter_and(content=self.unicode_ansj(self.cleaned_data['scontent']))

        """
        # 保证 *:* 显示正常 不需搜索查询分词
        """
        if self.cleaned_data.get('q') != "*:*" and self.cleaned_data.get('q'):
            boostkq = unicode(self.query_ansj_token(self.cleaned_data['q']), "UTF-8")
            # sqs = sqs.filter_and(text=boostkq)
            sqs = sqs.filter_and(SQ(title=self.unicode_ansj(self.cleaned_data['q'])) | \
                                 SQ(text=self.unicode_ansj(self.cleaned_data['q'])))

        return sqs.highlight()


class SearchForm_grzx(FacetedSearchForm, HighlightedSearchForm):
    order_by_time = forms.IntegerField(required=False)
    start_applytime = forms.CharField(required=False)
    end_applytime = forms.CharField(required=False)
    autolink = forms.CharField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SearchForm_grzx, self).search()
        # print "处理前",sqs.count()
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['order_by_time'] == 1:
            sqs = sqs.filter_and(webid='2').order_by('-textdate')
        else:
            sqs = sqs.filter_and(webid='2').order_by('-_score')

        # if self.cleaned_data['autolink'] :
        #     sqs = sqs.filter_and(autolink=self.cleaned_data['autolink'])

        # Check to see if a start_date was chosen.
        if sqs.count() == 0:
            pass
        else:
            if self.cleaned_data['start_applytime'] and self.cleaned_data['end_applytime']:
                sqs = sqs.filter_and(textdate__gte=self.cleaned_data['start_applytime'],
                                     textdate__lte=self.cleaned_data['end_applytime'])
        return sqs


class SearchForm_gdemo(FacetedSearchForm, HighlightedSearchForm):
    order_by_time = forms.IntegerField(required=False)
    start_applytime = forms.CharField(required=False)
    end_applytime = forms.CharField(required=False)
    autolink = forms.CharField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SearchForm_gdemo, self).search()
        # print "处理前",sqs.count()
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['order_by_time'] == 1:
            sqs = sqs.filter_and(webid='4').order_by('-textdate')
        else:
            sqs = sqs.filter_and(webid='4').order_by('-_score')

        # if self.cleaned_data['autolink'] :
        #     sqs = sqs.filter_and(autolink=self.cleaned_data['autolink'])

        # Check to see if a start_date was chosen.
        if sqs.count() == 0:
            pass
        else:
            if self.cleaned_data['start_applytime'] and self.cleaned_data['end_applytime']:
                sqs = sqs.filter_and(textdate__gte=self.cleaned_data['start_applytime'],
                                     textdate__lte=self.cleaned_data['end_applytime'])
        return sqs


class SearchForm_gdqzlx(FacetedSearchForm, HighlightedSearchForm):
    order_by_time = forms.IntegerField(required=False)
    start_applytime = forms.CharField(required=False)
    end_applytime = forms.CharField(required=False)
    autolink = forms.CharField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SearchForm_gdqzlx, self).search()
        # print "处理前",sqs.count()
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['order_by_time'] == 1:
            sqs = sqs.filter_and(webid='5').order_by('-textdate')
        else:
            sqs = sqs.filter_and(webid='5').order_by('-_score')

        # if self.cleaned_data['autolink'] :
        #     sqs = sqs.filter_and(autolink=self.cleaned_data['autolink'])

        # Check to see if a start_date was chosen.
        if sqs.count() == 0:
            pass
        else:
            if self.cleaned_data['start_applytime'] and self.cleaned_data['end_applytime']:
                sqs = sqs.filter_and(textdate__gte=self.cleaned_data['start_applytime'],
                                     textdate__lte=self.cleaned_data['end_applytime'])
        return sqs


class SearchForm_gdaiguo(FacetedSearchForm, HighlightedSearchForm):
    order_by_time = forms.IntegerField(required=False)
    start_applytime = forms.CharField(required=False)
    end_applytime = forms.CharField(required=False)
    autolink = forms.CharField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SearchForm_gdaiguo, self).search()
        # print "处理前",sqs.count()
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['order_by_time'] == 1:
            sqs = sqs.filter_and(webid='6').order_by('-textdate')
        else:
            sqs = sqs.filter_and(webid='6').order_by('-_score')

        # if self.cleaned_data['autolink'] :
        #     sqs = sqs.filter_and(autolink=self.cleaned_data['autolink'])

        # Check to see if a start_date was chosen.
        if sqs.count() == 0:
            pass
        else:
            if self.cleaned_data['start_applytime'] and self.cleaned_data['end_applytime']:
                sqs = sqs.filter_and(textdate__gte=self.cleaned_data['start_applytime'],
                                     textdate__lte=self.cleaned_data['end_applytime'])
        return sqs


class SearchForm_gdzf(FacetedSearchForm, HighlightedSearchForm):
    order_by_time = forms.IntegerField(required=False)
    start_applytime = forms.CharField(required=False)
    end_applytime = forms.CharField(required=False)
    autolink = forms.CharField(required=False)





    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SearchForm_gdzf, self).search()
        # print "处理前",sqs.count()
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['order_by_time'] == 1:
            sqs = sqs.filter_and(webid='7').order_by('-textdate')
        else:
            sqs = sqs.filter_and(webid='7').order_by('-_score')

        # if self.cleaned_data['autolink'] :
        #     sqs = sqs.filter_and(autolink=self.cleaned_data['autolink'])

        # Check to see if a start_date was chosen.
        if sqs.count() == 0:
            pass
        else:
            if self.cleaned_data['start_applytime'] and self.cleaned_data['end_applytime']:
                sqs = sqs.filter_and(textdate__gte=self.cleaned_data['start_applytime'],
                                     textdate__lte=self.cleaned_data['end_applytime'])
        return sqs


class ExcludeSearchForm(FacetedSearchForm, HighlightedSearchForm):
    excludewords = forms.CharField(required=False)

    def search(self):
        sqs = super(ExcludeSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['excludewords']:
            sqs = sqs.exclude(content=self.cleaned_data['excludewords'])

        return sqs

class SearchForm_maoming(FacetedSearchForm, HighlightedSearchForm):
    order_by_time = forms.IntegerField(required=False)
    start_applytime = forms.CharField(required=False)
    end_applytime = forms.CharField(required=False)
    autolink = forms.CharField(required=False)

    timezone.activate(pytz.timezone('Asia/Shanghai'))

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SearchForm_maoming, self).search()
        # print "处理前",sqs.count()
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['order_by_time'] == 1:
            sqs = sqs.filter_and(webid='31').order_by('-textdate')
        else:
            sqs = sqs.filter_and(webid='31').order_by('-_score')

        # if self.cleaned_data['autolink'] :
        #     sqs = sqs.filter_and(autolink=self.cleaned_data['autolink'])

        # Check to see if a start_date was chosen.
        if sqs.count() == 0:
            pass
        else:
            if self.cleaned_data['start_applytime'] and self.cleaned_data['end_applytime']:
                sqs = sqs.filter_and(textdate__gte=self.cleaned_data['start_applytime'],
                                     textdate__lte=self.cleaned_data['end_applytime'])

        return sqs