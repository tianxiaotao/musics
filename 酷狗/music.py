#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2024/4/10 16:11
# @Author : Carey
# @File : 音频下载.py
# @Description

import requests
import time
import hashlib

headers = {
    'accept': '*/*',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7',
    'origin': 'https://www.kugou.com',
    'referer': 'https://www.kugou.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

cookie = {
    "kg_mid": "df8eb959431e3f2696fc23d514fd9bf4",
    "kg_dfid": "3exIvy0NDCiI1x9u9X0MmaUX",
}

### 构建参数
###  encode_album_audio_id 歌曲短链  可由歌曲详情页链接后缀拿到
params = {
    'srcappid': '2919',
    'clientver': '20000',
    'clienttime': str( round(time.time()*1000) ),
    'mid': cookie['kg_mid'],
    'uuid': cookie['kg_mid'],
    'dfid': cookie['kg_dfid'],
    'appid': '1014',
    'platid': '4',
    'encode_album_audio_id': 'a9ton4f5',
    'token': '',
    'userid': '0',
}

arrKeys = []
for key in params:
    arrKeys.append( key )

arrKeys.sort()

u = 'NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt'
strRegParams = u
for key in arrKeys:
    strRegParams += f"{key}={params[key]}"

strEnc = strRegParams + u
signature = hashlib.md5( strEnc.encode(encoding='UTF-8')).hexdigest()
params[ 'signature' ] = signature

response = requests.get('https://wwwapi.kugou.com/play/songinfo', params=params, headers=headers)
print( response )
print( response.json() )