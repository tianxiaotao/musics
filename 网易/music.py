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
    #'cookie': 'MUSIC_U=00A9A1B6FE6B2C059DC454D26CFD3E5A83111232A90CC6E0F681AA424BA232617E038FC1AC62BC7001FEA04E89AFD1433BC9C03EB8BE45AE7E18508D52D33D50B647320C4E57C9F0F18DC0AAB11E1DFDE3730AAB617C61CE6D7D55B84E04FF5886D95561C5B245417B6C7009F51B7915D51E4AF3105603C74F037DC4B35A9FE8C34B85A1B1B36DB6B5C54B893C75A567094AE8095062DDB7570E560E46E0BB7167A428A5A8DA92C34B9740ECE929A8DCB5A981FFF991D3823CB8958F3BD6B1395C511EA0A37F2909AC4991A76FA5E9CB48DF189352B3009BD07F8135C4F63439437A118C2076803B00FDC74225EC35D10946490A5E7563651640A110C9407499452ECB956F3214C8BE987B5A4AEDA7B5D21FF077C06F02E2B7FA642B8F83C5C4C467E039F6E0F3C32E9A664AB9A6F3E4706EC1074EFE781531BD5F78A97B335262A3BB492B5DB3945503AB4E705B6B946CF87188E305D8704BAB2780FFB0B6A289CA4C3DFFA95966B14AA847F31C57D4BE53646916053552940E0FBD02775DBC82E7864427738DD3D3603AB5B035BC3E508EAAA0CEC938DD264B0EC340087EDE369B93F7DFC287935A14B6190A88651CB2D577F14C88685E753164029381DAAB59E6DD1354B7E0E9BBEDC2874A59AEC3804F6B48311A9CA32177C37A8018888D4FCC717ACB90834DB5BF2DF2112490B89C',
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