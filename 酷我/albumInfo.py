#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2024/6/6 11:10
# @Author : Carey
# @File : music.py
# @Description
import os.path
import re
import time

import requests

iTime = int( time.time() * 1000 )

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7',
    'Referer': 'https://www.kuwo.cn/album_detail/10250871',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Cookie': 'Hm_Iuvt_cdb524f42f23cer9b268564v7y735ewrq2324=BD5xXAhDfrjHNthect6BxJtZ3PfJyQMX',
    'Secret': '6114beda4966006fb857cad905ced9486bbbc7954fb0e85d3ad01dd3ffd728d405947f75'
}


def downloadAudio( url, path = None, fname = None ):

    response = requests.get( url, stream=True)
    response.encoding = 'utf-8'
    if 206 == response.status_code or 200 == response.status_code:
        with open(f'./{path}/{fname}.mp3', 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f'下载完成: {fname}.mp3')
        return True

    print('下载异常，访问源始文件失败')
    return False


def getDownloadAudio( aid, path = None, fname = None ):

    params = {
        'mid': aid,
        'type': 'music',
        'httpsStatus': '1',
        'reqId': 'f4e5d380-23da-11ef-8665-f1ea6239b94e',
        'plat': 'web_www',
        'from': '',
    }
    headers[ 'Referer' ] = f'https://www.kuwo.cn/play_detail/{aid}'
    headers[ 'Secret' ] = 'dec6468c32317e82f2cffb02b55c454a072484a682aeeebbb42715537828287b00007676'
    headers[ 'Cookie' ] = 'Hm_Iuvt_cdb524f42f23cer9b268564v7y735ewrq2324=JQsnHB8TNdKadMfyawpmDB4MX34ak8J8'

    response = requests.get('https://www.kuwo.cn/api/v1/www/music/playUrl', params=params, headers=headers)
    if 200 == response.status_code:
        resResult = response.json()
        if 'code' in resResult and -1 == resResult['code']:

            print(f"FNAME:{fname}, 下载链接未识别到. 【ERROR】-----{resResult['msg']}------")
            return False

        if 'url' in resResult[ 'data' ] and resResult[ 'data' ][ 'url' ] and len( resResult[ 'data' ][ 'url' ] ) > 0:
            downloadAudio( resResult[ 'data' ][ 'url' ], path, fname )
        else:
            print( f"FNAME:{fname}, 下载链接未识别到 ." )
    else:
        print(f'FNAME:{fname}, 音频接口请求异常 - {response.status_code}.')
    return True


def reqAudioByPage( bookid, page ):
    params = {
        'albumId': bookid,
        'pn': page,
        'rn': '20',
        'httpsStatus': '1',
        'reqId': '33121da0-23b6-11ef-87d3-6bfe8276b329',
        'plat': 'web_www',
        'from': '',
    }
    response = requests.get( 'https://www.kuwo.cn/api/www/album/albumInfo', params=params, headers=headers )
    if 200 == response.status_code:
        print( response.text )
        for item in response.json()[ 'data' ][ 'musicList' ]:
            if item['songTimeMinutes'] < '1:00':
                continue

            arrPath = re.findall(r'第(.*?)第', item['name'] )
            path = f"第{arrPath[0]}"
            if False == os.path.exists( os.getcwd() + '\\' + path.strip() ):
                os.mkdir( os.getcwd() + '\\' + path.strip() )

            arrFile = re.findall( r'第(\d+)章', item['name'] )
            fname = f"周建龙-{arrFile[0]}"

            if True == os.path.exists( os.getcwd() + '\\' + path.strip() + '\\' + f"{fname}.mp3" ):
                print(f"BOOK:{bookid}，PAGE:{page}，RID:{item['rid']}，NAME:{item['name']}，TIME:{item['songTimeMinutes']} 【Warning】 ----文件已存在--- " )
                print(' -----------------------------------  ')
                continue

            print(f"BOOK:{bookid}，PAGE:{page}，RID:{item['rid']}，NAME:{item['name']}，TIME:{item['songTimeMinutes']}")
            getDownloadAudio( item['rid'], path.strip(), fname )
            print( ' -----------------------------------  ' )


if __name__ == '__main__':

    getDownloadAudio( 279292599 )

    # bookid = 10250871
    # for i in range( 1, 16 ):
    #     page = i+1
    #     reqAudioByPage( bookid, page )
    #     break