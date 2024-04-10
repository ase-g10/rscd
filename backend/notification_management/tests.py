from channels.testing import ChannelsLiveServerTestCase
import websockets
import asyncio

class MyWebSocketTests(ChannelsLiveServerTestCase):
    async def test_my_consumer(self):
        async with websockets.connect(self.live_server_url) as websocket:
            # 发送消息
            await websocket.send("hello")
            # 接收响应
            response = await websocket.recv()
            self.assertEqual(response, "echo: hello")
