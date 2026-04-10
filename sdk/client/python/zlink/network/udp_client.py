# ZLink 비동기 UDP 트랜스포트 핸들러 - v13.2
import asyncio
import logging
import struct
from .tcp_client import HEADER_SIZE, HEADER_FMT, MAGIC_ZO

logger = logging.getLogger("zlink")

class AsyncUdpClient:
    """
    엔진 내부에서 사용되는 UDP 전송기입니다.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.transport = None
        self.unmarshaler = None
        self._running = False

    def set_unmarshaler(self, callback):
        self.unmarshaler = callback

    async def start(self):
        loop = asyncio.get_running_loop()
        try:
            self.transport, _ = await loop.create_datagram_endpoint(
                lambda: self._protocol_factory(),
                remote_addr=(self.host, self.port)
            )
            self._running = True
            return True
        except Exception as e:
            logger.error(f"[UDP] 시작 실패: {e}")
            return False

    async def stop(self):
        self._running = False
        if self.transport:
            self.transport.close()

    async def send(self, data: bytes):
        if not self.transport or not self._running: return
        self.transport.sendto(data)

    def _protocol_factory(self):
        outer = self
        class ZLinkUdpProtocol(asyncio.DatagramProtocol):
            def datagram_received(self, data, addr):
                if len(data) < HEADER_SIZE: return
                _, _, cmd, body_len, _, _, _ = struct.unpack(HEADER_FMT, data[:HEADER_SIZE])
                body = data[HEADER_SIZE : HEADER_SIZE+body_len] if body_len > 0 else b""
                if outer.unmarshaler:
                    outer.unmarshaler(cmd, body)

            def error_received(self, exc): logger.error(f"[UDP] 오류: {exc}")
        return ZLinkUdpProtocol()
