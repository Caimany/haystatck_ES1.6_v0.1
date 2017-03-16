import requests
http_code = requests.get('http://www.gd.gov.cn/gdgk/gdyw/201509/t20150922_218869.htm').status_code
print http_code
if http_code >= 400 and http_code <500:
    print "NO"