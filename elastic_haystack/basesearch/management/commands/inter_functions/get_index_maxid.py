# -*- coding:utf-8 -*-
from haystack.query import SearchQuerySet

def get(idname='id',**kwargs):
    return  SearchQuerySet().filter(**kwargs).order_by('-id')[0].id