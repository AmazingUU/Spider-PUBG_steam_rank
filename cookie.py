
filename = 'cookie.txt'
#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookie.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({
            'phone_num':'18019089182',
            'pwd':'3327921'
        })
#登录教务系统的URL
loginUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bks_login2.login'
#模拟登录，并把cookie保存到变量
result = opener.open(loginUrl,postdata)
#保存cookie到cookie.txt中
cookie.save(ignore_discard=True, ignore_expires=True)
#利用cookie请求访问另一个网址，此网址是成绩查询网址
gradeUrl = 'https://jwxt.sdu.edu.cn:7890/pls/wwwbks/bkscjcx.curscopre'
#请求访问成绩查询网址
result = opener.open(gradeUrl)
print(result.read())

# POST /account/login/?lang=zh-cn&os_type=iOS&os_version=10.3.3&_time=1548829094&version=1.1.52&device_id=D2AA4D4F-AC80-476C-BFE1-CBD83AB74133&heybox_id=-1&hkey=7c0718852ad0b14cdaf4e844f77ff98e HTTP/1.1
# Host: api.xiaoheihe.cn
# Referer: http://api.maxjia.com/
