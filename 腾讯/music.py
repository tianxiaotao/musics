#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2024/4/1 14:24
# @Author : Carey
# @File : 音频下载.py
# @Description
import base64
import json
import time
import requests
import execjs

headers = {
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://y.qq.com',
    'Referer': 'https://y.qq.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Cookie': 'qm_keyst=Q_H_L_63k3NZSrzisdN7i8VpHNUQgNjqjbJ1Da6PH71l9blwe3TrVY5-3bCLFjWuU8fpGgrNsAX_6pSakut98sPdS9L-Q; uin=120178015'
}

params = {
    '_': str( round( time.time() * 1000 ) ),
    'sign': 'zzcf90dd15ukaal7v2xwbp4yiumk8tr0wrugd3cf5f69',
}

with open( "item.js", "r", encoding='utf-8' ) as f:
    strEnc = f.read()

jsDrive = execjs.compile( strEnc )
strSchid = jsDrive.call( 'getSearchId', 1 )


mid = '002dw4gv1ZmiGt'

comm = {
    "cv":4747474,
    "ct":24,
    "format":"json",
    "inCharset":"utf-8",
    "outCharset":"utf-8",
    "notice":0,
    "platform":"yqq.json",
    "needNewCode":1,
    "uin":120178015,
    "g_tk_new_20200303":1380180348,
    "g_tk":1380180348
}
infoData = {
    "comm":comm,
    "req_1": {
        "module": "music.musicsearch.HotkeyService",
        "method": "GetHotkeyForQQMusicMobile",
        "param": {
            "searchid": strSchid,
            "remoteplace": "txt.yqq.top",
            "from": "yqqweb"
        }
    },
    "req_2":{
        "method": "get_song_detail_yqq",
		"module": "music.pf_song_detail_svr",
		"param": {
			"song_mid": mid
		}
    },
    "req_3":{
        "module": "music.paycenterapi.LoginStateVerificationApi",
		"method": "GetChargeAccount",
		"param": {
			"appid": "mlive"
		}
    }
}

strParam = json.dumps( infoData  )
sign = jsDrive.call( 'getEnc', strParam )
params[ 'sign' ] = sign
respDetailInfo = requests.post('https://u6.y.qq.com/cgi-bin/musics.fcg', params=params, headers=headers, data=strParam )
result = respDetailInfo.json()


songName = None
songID = None
songAbMid = None
companyName = None
pubTime = None
singers = ''
if result['req_2'][ 'data' ][ 'track_info' ]:
    songID = result['req_2'][ 'data' ][ 'track_info' ][ 'id' ]
    songAbMid = result['req_2'][ 'data' ][ 'track_info' ][ 'album' ][ 'mid' ]
    songName  = result['req_2'][ 'data' ][ 'extras' ][ 'name' ]

    if 'company' in result['req_2'][ 'data' ][ 'info' ]:
        companyName = result['req_2'][ 'data' ][ 'info' ][ 'company' ]['content'][0]['value']
    if 'pub_time' in result['req_2']['data']['info']:
        pubTime  = result['req_2'][ 'data' ][ 'info' ][ 'pub_time' ]['content'][0]['value']

    if result['req_2'][ 'data' ][ 'track_info' ][ 'singer' ]:
        for info in result['req_2'][ 'data' ][ 'track_info' ][ 'singer' ]:
            singers += f"{info['name']} / "

singers = singers.rstrip( ' / ' )

strGuid = jsDrive.call( 'getGuid' )
data = {
    "comm":comm,
    "req_1": {
		"module": "userInfo.VipQueryServer",
		"method": "SRFVipQuery_V2",
		"param": {
			"uin_list": ["0"]
		}
	},
    "req_2": {
		"module": "userInfo.BaseUserInfoServer",
		"method": "get_user_baseinfo_v2",
		"param": {
			"vec_uin": ["0"]
		}
	},
    "req_3": {
		"module": "music.lvz.VipIconUiShowSvr",
		"method": "GetVipIconUiV2",
		"param": {
			"PID": 3
		}
	},
    "req_4": {
		"module": "music.musicasset.SongFavRead",
		"method": "IsSongFanByMid",
		"param": {
			"v_songMid": [mid]
		}
	},
    "req_5": {
		"module": "music.musichallSong.PlayLyricInfo",
		"method": "GetPlayLyricInfo",
		"param": {
			"songMID":mid,
            "songID": songID
		}
	},
	"req_6": {
		"method": "GetCommentCount",
		"module": "music.globalComment.GlobalCommentRead",
		"param": {
			"request_list": [{
				"biz_type":1,
                "biz_id":str(songID),
                "biz_sub_type":0
			}]
		}
	},
	"req_7": {
		"module": "music.musichallAlbum.AlbumInfoServer",
		"method": "GetAlbumDetail",
		"param": {
			"albumMid": songAbMid
		}
	},
	"req_8": {
		"module": "music.vkey.GetVkey",
		"method": "GetUrl",
		"param": {
			"guid": strGuid,
			"songmid": [ mid ],
			"songtype": [0],
			"uin": "0",
			"loginflag": 1,
			"platform": "20"
		}
	}
}
strData = json.dumps( data ).replace(' ', '')

sign = jsDrive.call( 'getEnc', strData )
params[ 'sign' ] = sign
response = requests.post('https://u6.y.qq.com/cgi-bin/musics.fcg', params=params,  headers=headers, data= strData )

songInfo = response.json()
if 'sip' not in songInfo['req_1']['data'] or len( songInfo['req_1']['data']['sip'] ) <= 0:
    songInfo['req_1']['data']['sip'] = [
        "http://ws.stream.qqmusic.qq.com/",
        "http://isure.stream.qqmusic.qq.com/"
    ]


segment = songInfo['req_8']['data']['midurlinfo'][0]['purl']
if None == segment or len( segment ) <= 0:
    segment = songInfo['req_8']['data']['testfilewifi']

info = {
    'state': response.status_code,
    'id': songID,
    'code': mid,
    'name': songName,
    'album': songInfo['req_7']['data']['basicInfo']['albumName'],
    'lang': songInfo['req_7']['data']['basicInfo']['language'],
    'pubtime': pubTime,
    'singer': singers,
    'company': companyName,
    'servers': songInfo['req_1']['data']['sip'],
    'url': f"{songInfo['req_1']['data']['sip'][0]}{segment}",
    'lyric': base64.decodebytes( songInfo['req_5']['data']['lyric'].encode( 'utf-8' ) ).decode(),
}

if songInfo['req_7']['data']['singer']['singerList'] and len( songInfo['req_7']['data']['singer']['singerList'] ) > 0:
    info[ 'source' ] = songInfo['req_7']['data']['singer']['singerList'][0]['name']

print( info )