# haystatck_ES1.6_v0.1
初版的ES1.6普通检索接口,用于省直单位站点


#PIP
Django==1.8.6
MySQL-python==1.2.5
celery==3.1.18
charade==1.0.3
chardet==2.0.1
django-haystack==2.4.0
drf-haystack==1.5.5
elasticsearch==1.4.0
html5lib==0.999
lxml==3.4.4
requests==2.2.1
service-identity==14.0.0
simplejson==3.7.3
urllib3==1.14

优化更新索引   #redis-cli get custom_updated_id_multiple_search_engines |xargs -i  python /home/ubuntu/Haystack/elastic_haystack_multiplesite/elastic_haystack/manage.py custom_update_index --startid {} >> /home/ubuntu/log/cron_upindex.log 2>&1

条件更新索引   #python ./manage.py custom_update_filter --filed webid --filedkey 31