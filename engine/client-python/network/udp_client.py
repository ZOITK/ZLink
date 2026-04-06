import asyncio
from ..protocol.header import HeaderUDP
from ..logger.logger import logger

class AsyncUdpClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, on_receive=None):
        self.transport = None
        self.on_receive = on_receive

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if len(data) < 20:
            return

        try:
            header = HeaderUDP.decode(data[:20])
            body = data[20:] if header.length > 0 else b""
            
            if self.on_receive:
                if asyncio.iscoroutinefunction(self.on_receive):
                    asyncio.create_task(self.on_receive(header.command, body, header.sender, header.error))
                else:
                    self.on_receive(header.command, body, header.sender, header.error)
        except Exception as e:
            logger.error(f"[UDP] 패킷 처리 오류: {e}")

class AsyncUdpClient:
    def __init__(self, host, port, on_receive=None):
        self.host = host
        self.port = port
        self.on_receive = on_receive
        self.transport = None
        self.protocol = None

    async def start(self):
        try:
            loop = asyncio.get_event_loop()
            self.transport, self.protocol = await loop.create_datagram_endpoint(
                lambda: AsyncUdpClientProtocol(self.on_receive),
                remote_addr=(self.host, self.port)
            )
            logger.info(f"[UDP] 클라이언트 시작: {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"[UDP] 시작 실패: {e}")
            return False

    async def send(self, command, body=None, sender_idx=0, version=1):
        if not self.transport:
            return
        
        try:
            body_bytes = body if body else b""
            header = HeaderUDP(version, command, len(body_bytes), sender_idx, 0)
            data = header.encode() + body_bytes
            self.transport.sendto(data)
        except Exception as e:
            logger.error(f"[UDP] 패킷 전송 오류: {e}")

    async def close(self):
        if self.transport:
            self.transport.close()
        logger.info("[UDP] 클라이언트 종료")
