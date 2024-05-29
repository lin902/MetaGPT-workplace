import requests
from wxpusher import WxPusher  # https://github.com/wxpusher/wxpusher-sdk-python
import asyncio
from typing import Optional
import aiohttp
import os
from dataclasses import dataclass
import requests

from metagpt.schema import Message

app_token = 'AT_QCvbmgVKzgD8CVLhlKJD4Vb219WIvci9'   # 本处改成自己的应用 APP_TOKEN
uid_myself = 'UID_9o75Sx8kD1stxc6uMP5YKf1yzFWy'  # 本处改成自己的 UID

def wxpusher_send_by_webapi(msg):
    """利用 wxpusher 的 web api 发送 json 数据包，实现微信信息的发送"""
    webapi = 'http://wxpusher.zjiecode.com/api/send/message'
    data = {
        "appToken":app_token,
        "content":msg,
        "summary":msg[:99],  # 该参数可选，默认为 msg 的前10个字符
        "contentType": 1,
        "uids": [uid_myself, ],
        }
    result = requests.post(url=webapi, json=data)
    return result.text

def wxpusher_send_by_sdk(msg):
    """利用 wxpusher 的 python SDK ，实现微信信息的发送"""
    result = WxPusher.send_message(msg,
                 uids=[uid_myself],
                 token=app_token,
                 summary=msg[:99])
    return result


async def wxpusher_async_send(msg):
    return await asyncio.to_thread(WxPusher.send_message, msg, uids=[uid_myself], token=app_token)


async def main():
    msg = Message("Hello, WxPusher!!2")
    result = await wxpusher_async_send(msg)
    # 处理结果

if __name__ == "__main__":
    asyncio.run(main())



