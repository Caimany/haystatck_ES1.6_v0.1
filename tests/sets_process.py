# -*- coding:utf-8 -*-

index_pk_id = [[u'99397', u'basesearch.note.99397'], [u'99398', u'basesearch.note.99398'], [u'99391', u'basesearch.note.99391'], [u'99392', u'basesearch.note.99392'], [u'99396', u'basesearch.note.99396'], [u'99394', u'basesearch.note.99394'], [u'99393', u'basesearch.note.99393'], [u'99399', u'basesearch.note.99399'], [u'99395', u'basesearch.note.99395']]

qs_pk=[(99391L,), (99392L,), (99393L,), (99395L,), (99396L,), (99397L,), (99398L,), (99399L,)]


qs_set = set()

# for i, in qs_pk:
#      qs_set.add(str(i))
#
# for i,j in index_pk_id:
#     if i not in qs_set:
#         print 'i not in ...',i


#sort index_pk_id
s_1 = 0
for i, in qs_pk:
    s_1 = 0

    qs_set.add(str(i))