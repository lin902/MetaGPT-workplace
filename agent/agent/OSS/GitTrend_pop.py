import requests
from dotenv import load_dotenv
load_dotenv()
import asyncio
import aiohttp
import os
from dataclasses import dataclass


@dataclass
class Mess:
    content: str


class WxPusherClient:
    def __init__(
        self,
        token: str = None,
        base_url: str = "http://wxpusher.zjiecode.com",
    ):
        self.base_url = base_url
        self.token = token or os.getenv("WXPUSHER_TOKEN")

    async def send_message(
        self,
        content,
        summary: str = None,
        content_type: int = 1,
        topic_ids: list[int] = None,
        uids: list[int] = None,
        verify: bool = False,
        url: str = None,
    ):
        payload = {
            "appToken": self.token,
            "content": content,
            "summary": summary,
            "contentType": content_type,
            "topicIds": topic_ids or [],
            "uids": uids or [os.getenv("WXPUSHER_UIDS")],
            "verifyPay": verify,
            "url": url,
        }
        url = f"{self.base_url}/api/send/message"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                response.raise_for_status()
                return await response.text()

async def wxpusher_callback(msg: Mess):
    client = WxPusherClient()
    return await client.send_message(msg.content, content_type=3)


async def main():
    async def callback(msg):
        await wxpusher_callback(msg)

    with open("Codey_response.txt", "r") as file:
        file_content = file.read()
        # print("{file_content}")

    msg = Mess(content=file_content)
    await callback(msg)


if __name__ == "__main__":
    asyncio.run(main())
