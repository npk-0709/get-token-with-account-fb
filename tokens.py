import uuid
import requests
import random 
import string
import base64
import hashlib
import struct
import hmac
import time

def sort(dictionary):
    sor = sorted(dictionary.keys())
    data = {}
    for key in sor:
        data[key] = dictionary[key]
    return data

import hashlib

def encodesig(dictionary:dict):
    data = ''
    for info in dictionary:
        data += info + '=' + str(dictionary[info])
    data = md5(data + '62f8ce9f74b12f84c123cc23437a4a32')
    return data

def md5(string):
    return hashlib.md5(string.encode()).hexdigest()

def GooogleAuthenticator(code):
    intervals_no = int(time.time())//30
    key = base64.b32decode(code, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(string.ascii_letters) for i in range(length))
    
    # //EAAClA:   181425161904154|95a15d22a0e735b2983ecb9759dbaf91
    # //EAAAAU:   350685531728|62f8ce9f74b12f84c123cc23437a4a32
    # //EAADo1:   256002347743983|374e60f8b9bb6b8cbb30f78030438895
    # //EAAGO:    438142079694454|fc0a7caa49b192f64f6f5a6d9643bb28
    # //EAAAAAY:  6628568379|c1e620fa708a1d5696fb991c1bde5662
    # //EAAVB:    1479723375646806|afb3e4a6d8b868314cc843c21eebc6ae
    # //EAAC2S:   200424423651082|2a9918c6bcd75b94cefcbb5635c6ad16
    # //EAATK:    1348564698517390|007c0a9101b9e1c8ffab727666805038
    # //EAAQr:    1174099472704185|0722a7d5b5a4ac06b11450f7114eb2e9
    # //EAAI7:    628551730674460|b9693d3e013cfb23ec2c772783d14ce8
    # //EAAD6V7:  https://api.facebook.com/method/auth.getSessionforApp?format=json&access_token={token}&new_app_id=275254692598279
    # //thay vào access_token bên dưới để ra dạng token tương ứng 

def index():
    #100088845624129|2312230691hhbka|KATD2QXOGEPRAAFB5XKXZ2R4ZTOFGMJE|izsoldraskali@hotmail.com|Gp3cZ500||07/07/2008|1245609 | VND|2023-09-23T07:37:23+0700|58|http://103.188.166.248//Anh/100088845624129.jpg
    username = '100088845624129'
    password = '2312230691hhbka'
    _2fa = 'KATD2QXOGEPRAAFB5XKXZ2R4ZTOFGMJE'
    form = {
        
        "adid": str(uuid.uuid4()),
        "email": username,
        "password": password,
        "format": "json",
        "device_id": str(uuid.uuid4()),
        "cpl": "true",
        "family_device_id": str(uuid.uuid4()),
        "locale": "vi_VN",
        "client_country_code": "VN",
        "credentials_type": "device_based_login_password",
        "generate_session_cookies": "1",
        "generate_analytics_claim": "1",
        "generate_machine_id": "1",
        "currently_logged_in_userid": "0",
        "irisSeqID": 1,
        "try_num": "1",
        "enroll_misauth": "false",
        "meta_inf_fbmeta": "NO_FILE",
        "source": "login",
        "machine_id": ''.join(random.choice(string.ascii_letters) for i in range(24)),
        "meta_inf_fbmeta": "",
        "fb_api_req_friendly_name": "authenticate",
        "fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler",
        "api_key": "882a8490361da98702bf97a021ddc14d",
        "access_token": "350685531728%7C62f8ce9f74b12f84c123cc23437a4a32",
    }
    form.update({'sig':encodesig(sort(form))})
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "x-fb-friendly-name": form["fb_api_req_friendly_name"],
        "x-fb-http-engine": "Liger",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "cookie": "c_user=100093399498692; xs=27:S0WqWMhPutAwXw:2:1686753391:; m_page_voice=100093399498692; datr=b9CJZIWqtgAchUvJHMNEiXdT; fr=0QFyZdvXNZzTBBkWV.AWWDxSNplUPPlCgYmuGV2yM8XNM.BkidBv..AAA.0.0.BkidBv.AWVx4KpS0LU; sb=LReQZLiCNuYaiCsKJYLfn27J"
    }

    options = {
        "url": "https://b-graph.facebook.com/auth/login",
        "method": "post",
        "data": form,
        "headers": headers
    }

    response = requests.request(**options)
    print(response.json())
    if response.json()['error']['code'] == 406:
        form['credentials_type'] = 'two_factor'
        form['machine_id'] = response.json()['error']['error_data']['machine_id']
        form.update({'encrypted_msisdn':''})
        form.update({'userid':response.json()['error']['error_data']['uid']})
        form.update({'twofactor_code':str(GooogleAuthenticator(_2fa))})
        form.update({'login_first_factor':response.json()['error']['error_data']['login_first_factor']})
        form['sig'] = encodesig(sort(form))
        print(form)
    options = {
        "url": "https://b-graph.facebook.com/auth/login",
        "method": "post",
        "data": form,
        "headers": headers
    }

    response = requests.request( **options)

    print(response.text)

            
index()
