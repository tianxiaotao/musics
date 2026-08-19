import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")

from threading import Thread
from tqdm import tqdm
import os.path
import re
import time
import requests
from lxml import etree
import execjs
import random
from urllib.parse import urlencode, quote


iTime = time.time()

headers_list = [
    {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.37'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.40',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.44',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.58',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.72',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.93',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.97',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.61',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.77',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.89',
    }, {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.91',
    }
]


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en',
    'Referer': 'http://www.yuetingba.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
}


def downloadAudio( path, fname, url ):
    headers[ 'Referer' ] = 'http://www.yuetingba.cn/'
    headers[ 'Accept' ] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    headers[ 'Accept-Encoding' ] = 'gzip, deflate'
    headers[ 'Accept-Language' ] = 'zh-CN,zh;q=0.9,en;q=0.8'
    headers[ 'User-Agent' ] =  random.choice(headers_list)[ 'user-agent' ]

    try:
        response = requests.get(url, headers=headers, stream=True)
        if 206 == response.status_code or 200 == response.status_code:
            file_size = int(response.headers['Content-Length'])
            chunk_size = 30720
            num_bars = int(file_size / chunk_size)
            with open(f'./{path}/{fname}', 'wb') as f:
                for chunk in tqdm(response.iter_content(chunk_size=chunk_size), total=num_bars, unit='KB', desc=fname,
                                  leave=True):
                    f.write(chunk)

            response.close()
            print(f'下载完成: {fname}')
            return True

        response.close()
        print('下载异常，访问源始文件失败')
    except ( requests.exceptions.ChunkedEncodingError, requests.ConnectionError ) as e:
        print( f'ERROR. Path:{path}/{fname}  Msg:{e}' )
        os.remove( f'./{path}/{fname}' )

        t = Thread(target=downloadAudio, args=(path, fname,  url ))
        t.start()

    return False


def getDownloadAudio( no, path, fname ):

    headers['Referer'] = 'http://www.yuetingba.cn/tingpage/index.html'
    headers['Accept'] = 'application/json, text/plain, */*'
    headers['Accept-Language'] = 'en'

    response = requests.get( f'http://www.yuetingba.cn/api/app/docs-listen/{no}/ting-with-ef', headers=headers )
    if 200 != response.status_code:
        print( f"剧集编号：{no}  预计下载：【位置】 - {path}，【名称】-{fname} 【ERROR】 ----请求接口失败：{response.status_code}--- ")

    result = response.json()
    print( f"获取剧集：{result['title']}，剧集编号：{result['id']}，密文已获取完成，开始解密 ")

    with open( 'aes.js', 'r', encoding='utf-8' ) as f:
        js_tamp = f.read()

    jsDrive = execjs.compile( js_tamp )
    strEncLink = jsDrive.call( 'aesDecryptBase64', 'le95G3hnFDJsBE+1/v9eYw==', result['ef'], 'IvswQFEUdKYf+d1wKpYLTg==' )
    print(f"获取剧集：{result['title']}，剧集编号：{result['id']}，解密已完成：{strEncLink} --- 开始下载--- ")
    t = Thread(target=downloadAudio, args=(path, fname, f"http://117.65.19.124:50010{quote(strEncLink)}"))
    t.start()

def download( id, num ):
    request = requests.get( f'http://www.yuetingba.cn/book/detail/{id}/{num}', headers=headers )
    request.encoding = 'utf-8'
    if 500 == request.status_code:
        print('下载异常，访问源站点失败')
        return False

    html = etree.HTML( request.text )
    wapperContent = html.xpath( "//div[@class='ting-list']/div[@class='ting-list-content row']/div[@class='col-md-3 col-xs-12']" )

    for item in wapperContent:
        name = item.xpath( ".//div[@class='col-md-10 col-xs-10']/a/text()" )[0]
        strNo = item.xpath( ".//div[@class='col-md-10 col-xs-10']/a/@onclick" )[0]
        no = re.findall( r'\'(.*?)\'', strNo, re.S )[0]

        try:
            arrInfo = re.findall(r'(.*?)(\d+)', name.split('-')[1], re.S)[0]
            path = arrInfo[0]
            fname = f"{arrInfo[1]}.mp3"
        except Exception as e:
            path = html.xpath( "//h1[@class='hidden-xs']/text()" )[0]
            subPath = name.split( '_' )
            fname = f"{subPath[0]}.mp3"
            sub = subPath[1]
            path =  path.strip() + '\\' + sub.strip()

        if False == os.path.exists(os.getcwd() + '\\' + path.strip()):
            os.mkdir(os.getcwd() + '\\' + path.strip())

        if True == os.path.exists(os.getcwd() + '\\' + path.strip() + '\\' + f"{fname}"):
            print( f"获取剧集：{name}，剧集编号：{no}  预计下载：【位置】-{path.strip()}，【名称】-{fname.strip()} 【WARNING】 ----文件已存在--- ")
            print(' -----------------------------------  ')
            fsize = os.stat( os.getcwd() + '\\' + path.strip() + '\\' + f"{fname}" ).st_size
            mSize = round( fsize/(1024**2), 2 )
            print( f"获取剧集：{name}，剧集编号：{no}  预计下载：【位置】-{path.strip()}，【名称】-{fname.strip()} 【检测文件大小】 ----{mSize}MB---" )
            if mSize > 1:
                continue

            print( f"获取剧集：{name}，剧集编号：{no}  预计下载：【位置】-{path.strip()}，【名称】-{fname.strip()} 【文件检测不通过】 已删除文件重新下载" )
            os.remove( os.getcwd() + '\\' + path.strip() + '\\' + f"{fname}" )

        print( f"获取剧集：{name}，剧集编号：{no}  预计下载：【位置】-{path.strip()}，【名称】-{fname.strip()}" )
        getDownloadAudio( no, path.strip(), fname.strip() )


###  http://www.yuetingba.cn
if __name__ == '__main__':

    #bookid = '3a049826-dea5-5490-a73c-d4343bce1b39' # 盗墓笔记
    bookid = '3a074091-9338-a6e1-d74c-ef1142f0734c'  # 剑来
    page = input( '请输入页码?' )
    if None == page or len( page ) <= 0 :
        page = 1200

    download( bookid, page )