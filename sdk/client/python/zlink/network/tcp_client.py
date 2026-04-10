# ZLink 비동기 TCP 트랜스포트 핸들러 - v13.2
import asyncio
import logging
import struct

logger = logging.getLogger("zlink")

# ZLink 표준 규격 (SSOT)
HEADER_SIZE = 24
MAGIC_ZO = 0x4F5A
HEADER_FMT = "<HIIIIIH"  # Magic(H), Ver(I), Cmd(I), Len(I), Sess(I), Err(I), Seq(H)

def Pack(cmd_id: int, body: bytes, session_id: int = 0, error_code: int = 0, version: int = 1) -> bytes:
    """ZLink 24바이트 표준 패킷을 조립합니다."""
    hdr = struct.pack(HEADER_FMT, MAGIC_ZO, version, cmd_id, len(body), session_id, error_code, 0)
    return hdr + body

class _TcpClient:
    """
    엔진 내부에서 사용되는 TCP 전송기입니다.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.unmarshaler = None # 실제로는 엔진의 디스패처가 주입됨
        self._running = False
        self.session_id = 0  # 서버로부터 할당받은 SessionID

    def set_unmarshaler(self, callback):
        self.unmarshaler = callback

    async def start(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            self._running = True
            asyncio.create_task(self._receive_loop())
            return True
        except Exception as e:
            logger.error(f"[TCP] 연결 실패: {e}")
            return False

    async def stop(self):
        self._running = False
        if self.writer:
            self.writer.close()
            try: await self.writer.wait_closed()
            except: pass
        logger.info("[TCP] 종료")

    async def send(self, data: bytes):
        if not self.writer or not self._running: return
        self.writer.write(data)
        await self.writer.drain()

    async def _receive_loop(self):
        try:
            while self._running:
                hdr_data = await self.reader.readexactly(HEADER_SIZE)
                if not hdr_data: break

                _, _, cmd, body_len, session_id, _, _ = struct.unpack(HEADER_FMT, hdr_data)
                body = await self.reader.readexactly(body_len) if body_len > 0 else b""

                if self.unmarshaler:
                    # session_id를 함께 전달하여 엔진이 학습하도록 함
                    self.unmarshaler(cmd, body, session_id)

        except asyncio.IncompleteReadError:
            pass
        except Exception as e:
            if self._running: logger.error(f"[TCP] 수신 오류: {e}")
        finally:
            self._running = False
