#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2024/3/21 10:05
# @Author : Carey
# @File : 音频下载.py
# @Description
import json

import requests
import execjs

headers = {
    'accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://music.163.com',
    'referer': 'https://music.163.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
}

with open( "item.js", "r", encoding='utf-8' ) as f:
    strEnc = f.read()


iMusidId = 865632948
jsDrive = execjs.compile( strEnc )
objResult = jsDrive.call( 'getMusicEnc', [iMusidId] )

data = {
    'params': objResult[ 'encText' ],
    'encSecKey': objResult[ 'encSecKey' ],
}
response = requests.post( 'https://music.163.com/weapi/song/enhance/player/url/v1', headers=headers, data=data )
print( response )
print( response.text )

param = {
    'csrf_token': '',
    'id': iMusidId,
    'lv': -1,
    'tv': -1
}
objLyric = jsDrive.call( 'getMusicLyricEnc', param )
lyricData = {
    'params': objLyric[ 'encText' ],
    'encSecKey': objLyric[ 'encSecKey' ],
}

res = requests.post( 'https://music.163.com/weapi/song/lyric', headers = headers, data= lyricData  )
print( res )
print( res.text )
