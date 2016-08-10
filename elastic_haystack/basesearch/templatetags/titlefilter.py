__author__ = 'Caimany'
# -*- coding: utf-8 -*-
from django import template
import re
register = template.Library()
@register.filter
def fzw_title(value):
    title=re.sub(r'\s泛珠三角合作信息网$','',value.encode("utf-8"))
    return unicode(title,"utf-8")
