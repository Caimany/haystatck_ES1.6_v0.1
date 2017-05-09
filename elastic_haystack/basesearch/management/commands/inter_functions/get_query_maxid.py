# encoding: utf-8
from basesearch.models import Note
from django.db.models import Max,Count

"""
       from zwgkapp.management.commands.inter_functions import get_query_maxid
        print(get_query_maxid.get(idname='id',city_num=0)
"""


def get(idname=id, **kwargs):
    """
    
    :param idname: 
    :param kwargs: 
    :return: 
    """
    datas = Note.objects.filter(**kwargs)
    return datas.aggregate(Max(idname))[idname + '__max']
