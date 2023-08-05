from os import path
import hashlib
import json
import requests
from requests.cookies import RequestsCookieJar
import http.cookiejar as cookielib
import lxml.html

def_userinfo = {
    'zyb' : {
        'username' : '18612866364',
        'password' : '111111',
    },
    'yike' : {
        'username' : '18612866364',
        'password' : '111111',
    },
    'parent' : {
        'username' : '13466730603',
        'randtoken' : '9527',
    },
    'kuaidui' : {
        'username' : '18612866364',
        'password' : '111111',
    },
}
zyb_file = "loginConf.py"
hosts = {
    #'zyb' : 'https://www.zybang.com/',
    #'parent' : 'https://jiazhang.zuoyebang.com/',
    #'kuaidui' : 'https://www.kuaiduizuoye.com/',
    #'yike' : 'https://www.zybang.com/',
    'zyb' : os.environ['URL'],
    'parent' : os.environ['URL'],
    'kuaidui' : os.environ['URL'],
    'yike' : os.environ['URL'],
    'cas' : os.environ['URL'],
}
header = {
    'Content-Type' : 'application/x-www-form-urlencoded',
    'User-Agent' : 'homework/11.6.4 (iPhone; iOS 12.1.2; Scale/2.00)',
}

def zyb_Login(arrInput = def_userinfo['zyb']):
    zybuss = ''
    arrOutput = {'zybuss' : zybuss}

    #填充username、password
    if (not arrInput. __contains__('username')) or (not arrInput['username']) or  (not arrInput. __contains__('password')):
        arrInput['username'] = def_userinfo['zyb']['username']
        arrInput['password'] = def_userinfo['zyb']['password']
    #因为端的密码就是MD5了两次，所以这一部分并不是我多写了一次
    arrInput['password'] = hashlib.md5(arrInput['password'].encode('utf-8')).hexdigest()
    arrInput['password'] = hashlib.md5(arrInput['password'].encode('utf-8')).hexdigest()

	#获取存储的zybuss
    with open(zyb_file, 'r') as conf:
        conf_str = conf.read()
        conf_arr = json.loads(conf_str)
    if conf_arr.__contains__('zyb') and conf_arr['zyb'].__contains__(hosts['zyb']) and conf_arr['zyb'][hosts['zyb']].__contains__(arrInput['username']) and conf_arr['zyb'][hosts['zyb']][arrInput['username']]:
        zybuss = conf_arr['zyb'][hosts['zyb']][arrInput['username']]

    #验证zybuss是否过期
    user_url = hosts['zyb'] + 'napi/user/userinfo?skip=rdqa'
    user_cookie = {'ZYBUSS' : zybuss,}
    user_data = {
        'zybuss' : zybuss,
        'token' : '2_XPXQH3c5HRPtFHkSwi3sCCURmT25QfxM',
        'sign' : '03db23d129b6dec7623fcd4b073d3a94',
        'appId' : 'homework',
        'bundleID' : 'com.baidu.homework',
    }
    res = requests.post(user_url, headers = header, data = user_data, cookies = user_cookie)
    if res.status_code != 200:
        return arrOutput
    try:
        res_data = json.loads(res.content.decode('utf-8'))
        print(res_data)
    except ValueError:
        return arrOutput

    #如果zybuss已过期，则重新登录
    if res_data['errNo'] != 0:
        #如果登录失败，则重试3次
        n = 0
        while n<3:
            login_url = hosts['zyb'] + 'session/submit/login?skip=rdqa'
            login_data = {
                'phone' : arrInput['username'],
                'password' : arrInput['password'],
                'token' : '2_XPXQH3c5HRPtFHkSwi3sCCURmT25QfxM',
                'sign' : '03db23d129b6dec7623fcd4b073d3a94',
                'appId' : 'homework',
                'bundleID' : 'com.baidu.homework',
            }
            res = requests.post(login_url, headers = header, data = login_data)
            if res.status_code != 200:
                n = n+1
                continue
            try:
                res_data = json.loads(res.content.decode('utf-8'))
                print(res_data)
            except ValueError:
                n = n+1
                continue
            if res_data['errNo'] == 0 and res_data['data']['zybuss'] != '':
                zybuss = res_data['data']['zybuss']
                #将新的zybuss写入文件
                conf_arr['zyb'][hosts['zyb']][arrInput['username']] = zybuss
                with open(zyb_file, 'w') as conf:
                    conf_str = json.dumps(conf_arr)
                    conf.write(conf_str)
                break;
            n = n+1;
    arrOutput['zybuss'] = zybuss
    return arrOutput

def parent_Login(arrInput = def_userinfo['parent']):
    zybuss = ''
    arrOutput = {'zybuss' : zybuss}

    #填充username
    if (not arrInput. __contains__('username')) or (not arrInput['username']) or (not arrInput. __contains__('randtoken')):
        arrInput['username'] = def_userinfo['parent']['username']
        arrInput['randtoken'] = def_userinfo['parent']['token']

    #获取存储的zybuss
    with open(zyb_file, 'r') as conf:
        conf_str = conf.read()
        conf_arr = json.loads(conf_str)
    if conf_arr.__contains__('parent') and conf_arr['parent'].__contains__(hosts['parent']) and conf_arr['parent'][hosts['parent']].__contains__(arrInput['username']) and conf_arr['parent'][hosts['parent']][arrInput['username']]:
        zybuss = conf_arr['parent'][hosts['parent']][arrInput['username']]

    #验证zybuss是否过期
    user_url = hosts['parent'] + 'parent/user/userinfo?skip=rdqa'
    user_cookie = {'ZYBUSS' : zybuss,}
    user_data = {
        'zybuss' : zybuss,
        'token' : '2_XPXQH3c5HRPtFHkSwi3sCCURmT25QfxM',
        'sign' : '0cf996f90dbda124b276b03cda92968d',
        'appId' : 'parent',
        'bundleID' : 'com.zybang.parent',
        'os' : 'ios',
    }
    res = requests.post(user_url, headers = header, data = user_data, cookies = user_cookie)
    if res.status_code != 200:
        return arrOutput
    try:
        res_data = json.loads(res.content.decode('utf-8'))
        print(res_data)
    except ValueError:
        return arrOutput

    #如果zybuss已过期，则重新登录
    if res_data['errNo'] != 0:
        #如果登录失败，则重试3次
        n = 0
        while n<3:
            login_url = hosts['parent'] + 'session/submit/tokenlogin?skip=rdqa'
            login_data = {
                'phone' : arrInput['username'],
                'randtoken' : arrInput['randtoken'],
                'token' : '2_XPXQH3c5HRPtFHkSwi3sCCURmT25QfxM',
                'sign' : '03db23d129b6dec7623fcd4b073d3a94',
                'appId' : 'parent',
                'bundleID' : 'com.zybang.parent',
                'os' : 'ios',
            }
            res = requests.post(login_url, headers = header, data = login_data)
            if res.status_code != 200:
                n = n+1
                continue
            try:
                res_data = json.loads(res.content.decode('utf-8'))
                print(res_data)
            except ValueError:
                n = n+1
                continue
            if res_data['errNo'] == 0 and res_data['data']['zybuss'] != '':
                zybuss = res_data['data']['zybuss']
                #将新的zybuss写入文件
                conf_arr['parent'][hosts['parent']][arrInput['username']] = zybuss
                with open(zyb_file, 'w') as conf:
                    conf_str = json.dumps(conf_arr)
                    conf.write(conf_str)
                break;
            n = n+1;
    arrOutput['zybuss'] = zybuss
    return arrOutput

def kuaidui_Login(arrInput = def_userinfo['kuaidui']):
    kduss = ''
    arrOutput = {'kduss' : kduss}

    #填充username、password
    #快对的登录密码竟然是明文传输的，厉害厉害！虽然用的是https，这也太任性了吧。。。
    if (not arrInput. __contains__('username')) or (not arrInput['username']) or  (not arrInput. __contains__('password')):
        arrInput['username'] = def_userinfo['kuaidui']['username']
        arrInput['password'] = def_userinfo['kuaidui']['password']
    
    #获取存储的kduss
    with open(zyb_file, 'r') as conf:
        conf_str = conf.read()
        conf_arr = json.loads(conf_str)
    if conf_arr.__contains__('kuaidui') and conf_arr['kuaidui'].__contains__(hosts['kuaidui']) and conf_arr['kuaidui'][hosts['kuaidui']].__contains__(arrInput['username']) and conf_arr['kuaidui'][hosts['kuaidui']][arrInput['username']]:
        kduss = conf_arr['kuaidui'][hosts['kuaidui']][arrInput['username']]

    #验证zkduss是否过期
    user_url = hosts['kuaidui'] + 'codesearch/user/userinfo?skip=rdqa'
    user_cookie = {'KDUSS' : kduss,}
    user_data = {
        'kduss' : kduss,
        'token' : '2_XPXQH3c5HRPtFHkSwi3sCCURmT25QfxM',
        'sign' : '89067c95ddbf4f40a44219167e2be912',
        'appId' : 'scancode',
        'bundleID' : 'com.kuaiduizuoye.scan',
    }
    res = requests.post(user_url, headers = header, data = user_data, cookies = user_cookie)
    if res.status_code != 200:
        return arrOutput
    try:
        res_data = json.loads(res.content.decode('utf-8'))
        print(res_data)
    except ValueError:
        return arrOutput

    #如果kduss已过期，则重新登录
    if res_data['errNo'] != 0:
        #如果登录失败，则重试3次
        n = 0
        while n<3:
            login_url = hosts['kuaidui'] + 'session/submit/login?skip=rdqa'
            login_data = {
                'phone' : arrInput['username'],
                'password' : arrInput['password'],
                'token' : '2_XPXQH3c5HRPtFHkSwi3sCCURmT25QfxM',
                'sign' : '89067c95ddbf4f40a44219167e2be912',
                'appId' : 'scancode',
                'bundleID' : 'com.kuaiduizuoye.scan',
            }
            res = requests.post(login_url, headers = header, data = login_data)
            if res.status_code != 200:
                n = n+1
                continue
            try:
                res_data = json.loads(res.content.decode('utf-8'))
                print(res_data)
            except ValueError:
                n = n+1
                continue
            if res_data['errNo'] == 0 and res_data['data']['kduss'] != '':
                kduss = res_data['data']['kduss']
                #将新的kduss写入文件
                conf_arr['kuaidui'][hosts['kuaidui']][arrInput['username']] = kduss
                with open(zyb_file, 'w') as conf:
                    conf_str = json.dumps(conf_arr)
                    conf.write(conf_str)
                break;
            n = n+1;
    arrOutput['kduss'] = kduss
    return arrOutput

def yike_Login(arrInput = def_userinfo['yike']):
    zybuss = ''
    arrOutput = {'zybuss' : zybuss}

    #填充username、password
    if (not arrInput. __contains__('username')) or (not arrInput['username']) or  (not arrInput. __contains__('password')):
        arrInput['username'] = def_userinfo['yike']['username']
        arrInput['password'] = def_userinfo['yike']['password']
    #因为端的密码就是MD5了两次，所以这一部分并不是我多写了一次
    arrInput['password'] = hashlib.md5(arrInput['password'].encode('utf-8')).hexdigest()
    arrInput['password'] = hashlib.md5(arrInput['password'].encode('utf-8')).hexdigest()

    #获取存储的zybuss
    with open(zyb_file, 'r') as conf:
        conf_str = conf.read()
        conf_arr = json.loads(conf_str)
    if conf_arr.__contains__('yike') and conf_arr['yike'].__contains__(hosts['yike']) and conf_arr['yike'][hosts['yike']].__contains__(arrInput['username']) and conf_arr['yike'][hosts['yike']][arrInput['username']]:
        zybuss = conf_arr['yike'][hosts['yike']][arrInput['username']]

    #验证zybuss是否过期
    user_url = hosts['yike'] + 'course/user/userinfo?skip=rdqa'
    user_cookie = {'ZYBUSS' : zybuss,}
    user_data = {
        'zybuss' : zybuss,
        'token' : '2_XPXQH3c5HRPtFHkSwi3sCCURmT25QfxM',
        'sign' : '9459b1c82fc118d9bcba15816f968939',
        'appId' : 'airclass',
        'bundleID' : 'com.zuoyebang.student',
    }
    res = requests.post(user_url, headers = header, data = user_data, cookies = user_cookie)
    if res.status_code != 200:
        return arrOutput
    try:
        res_data = json.loads(res.content.decode('utf-8'))
        print(res_data)
    except ValueError:
        return arrOutput

    #如果zybuss已过期，则重新登录
    if res_data['errNo'] != 0:
        #如果登录失败，则重试3次
        n = 0
        while n<3:
            login_url = hosts['yike'] + 'session/submit/login?skip=rdqa'
            login_data = {
                'phone' : arrInput['username'],
                'password' : arrInput['password'],
                'token' : '2_XPXQH3c5HRPtFHkSwi3sCCURmT25QfxM',
                'sign' : '9459b1c82fc118d9bcba15816f968939',
                'appId' : 'airclass',
                'bundleID' : 'com.zuoyebang.student',
            }
            res = requests.post(login_url, headers = header, data = login_data)
            if res.status_code != 200:
                n = n+1
                continue
            try:
                res_data = json.loads(res.content.decode('utf-8'))
                print(res_data)
            except ValueError:
                n = n+1
                continue
            if res_data['errNo'] == 0 and res_data['data']['zybuss'] != '':
                zybuss = res_data['data']['zybuss']
                #将新的zybuss写入文件
                conf_arr['yike'][hosts['yike']][arrInput['username']] = zybuss
                with open(zyb_file, 'w') as conf:
                    conf_str = json.dumps(conf_arr)
                    conf.write(conf_str)
                break;
            n = n+1;
    arrOutput['zybuss'] = zybuss
    return arrOutput

def cas_Login(arrInput):
    CALLBACK_URL = arrInput['callback_url']
    LOGIN_URL = "https://cas.zuoyebang.cc/login"
    cas_data = {
        'username' : arrInput['username'],
        'password' : arrInput['password'],
    }
    cas_header = {
        "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "156",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "cas.zuoyebang.cc",
        "Referer": CALLBACK_URL,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"
    }
    event_headers = {
        "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Host": hosts['cas'],
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"
    }
    http_request = requests.session()
    http_response = http_request.get(CALLBACK_URL)
    html_content = http_response.text

    # parsing page for hidden inputs
    login_html = lxml.html.fromstring(html_content)
    hidden_inputs = login_html.xpath('//input[@type="hidden"]')
    user_form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    user_form["username"] = cas_data['username'];
    user_form["password"] = cas_data['password'];
    login_request = http_request.post(LOGIN_URL, data=user_form, headers=cas_header, allow_redirects=False)
    location = login_request.headers['Location']

    http_request.get(location, headers=event_headers)
    cookies = http_request.cookies.get_dict()

    return cookies
