from peewee import *

from django.conf import settings

import os
# db = SqliteDatabase('indexresults.db')
db = SqliteDatabase(os.path.join(settings.BASE_DIR, 'indexresults.db'))

class ErrorDetail(Model):
    time = DateTimeField()
    errorid = CharField()
    exceptions = CharField()

    class Meta:
        database = db

class IndexINFO(Model):
    starttime = DateTimeField()
    endtime = DateTimeField()
    city_num = IntegerField(primary_key=True,default=100)
    last_index_total = IntegerField()
    last_index_id = IntegerField()

    class Meta:
        database = db


