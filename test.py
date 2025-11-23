import urllib.parse
import random
import string

def enc_pwd(passIn, key):
    passOut = ""
    if not passIn:
        return passOut
    if len(passIn) > 512:
        return "-1"
    for i in range(len(passIn)):
        ch = ord(passIn[i]) ^ ord(key[i % len(key)])
        str_ch = format(ch, 'x')
        if len(str_ch) == 1:
            str_ch = "0" + str_ch
        passOut += str_ch
    return passOut

def getkey(ip):
    ret = 0
    for char in ip:
        ret ^= ord(char)
    return ret

def format_params(url,data, encryption_type, secret_key, term_ip):
    arr = []
    for name, value in data.items():
        if name == 'callback':
            arr.insert(0, urllib.parse.quote(name) + '=' + urllib.parse.quote(value))
        else:
            arr.append(urllib.parse.quote(name) + '=' + urllib.parse.quote(value))
    arr.append('v=' + str(random.randint(500, 10500)))
    arr.append('lang=zh')
    print(params['data']) 
    if encryption_type == '1' and 'drcom/chkstatus' not in url and 'drcom/login' not in url and 'drcom/getipv6' not in url and 'drcom/logout' not in url:
        keys = getkey(secret_key)
        encrypted_data = {}
        for key, value in data.items():
            if key != "error_code":
                encrypted_data[key] = enc_pwd(value, keys)
            else:
                encrypted_data[key] = value
        encrypted_data['encrypt'] = 1
        arr = []
        for name, value in encrypted_data.items():
            arr.append(urllib.parse.quote(name) + '=' + urllib.parse.quote(value))

    return '&'.join(arr)

# 示例数据
params = {
    'url': 'http://example.com/api',
    'data': {
        'user_account': 'myusername',
        'user_password': 'mypassword',
        'callback': 'callbackName'
    },
    'encryption_type': '1',
    'secret_key': 'drcom',
    'term_ip': '192.168.1.1'
}


formatted_params = format_params(params['url'],params['data'], params['encryption_type'], params['secret_key'], params['term_ip'])
print(formatted_params)
