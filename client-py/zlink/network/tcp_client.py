import asyncio
import io
import logging
import struct
from ..logger.logger import logger

class AsyncTcpClient:
    def __init__(self, Host, Port):
        self.Host = Host
        self.Port = Port
        self.Reader = None
        self.Writer = None
        self._Running = False
        
        # --- 핵심 개선: 엔진이 직접 프로토콜과 로직을 관리함 (Go와 동일) ---
        self.Unmarshaler = None
        self.OnRecvCallbacks = []
        
        # 헤더 정보 (제네레이터에 의해 설정됨)
        self.HeaderSize = 16
        self.HeaderDecoder = None

    def AddRecvCallback(self, Callback):
        """새로운 패킷 리스너를 추가합니다 (Go와 동일)"""
        self.OnRecvCallbacks.append(Callback)

    def SetUnmarshaler(self, Unmarshaler):
        """제네레이터가 호출하여 파싱 로직을 등록합니다."""
        self.Unmarshaler = Unmarshaler

    def SetHeaderInfo(self, HeaderSize, Decoder):
        """제네레이터가 호출하여 헤더 크기와 디코더를 등록합니다."""
        self.HeaderSize = HeaderSize
        self.HeaderDecoder = Decoder

    async def Connect(self):
        try:
            self.Reader, self.Writer = await asyncio.open_connection(self.Host, self.Port)
            self._Running = True
            logger.info(f"[TCP] 서버 연결 성공: {self.Host}:{self.Port}")
            asyncio.create_task(self._ReceiveLoop())
            return True
        except Exception as e:
            logger.error(f"[TCP] 연결 실패: {e}")
            return False

    async def Send(self, Data):
        """이미 인코딩된 로우 데이터를 전송합니다."""
        if not self.Writer or self.Writer.is_closing(): return
        try:
            self.Writer.write(Data)
            await self.Writer.drain()
        except Exception as e:
            logger.error(f"[TCP] 전송 오류: {e}")
            await self.Close()

    async def _ReceiveLoop(self):
        try:
            while self._Running:
                # 1. 헤더 읽기
                hdr_data = await self.Reader.readexactly(self.HeaderSize)
                
                cmd = 0
                body_len = 0
                
                if self.HeaderDecoder:
                    hdr = self.HeaderDecoder(hdr_data)
                    if not hdr: continue
                    cmd = hdr.Command
                    body_len = hdr.Length
                else:
                    # 기본값 (하위 호환성용 - Little Endian 강제)
                    v, cmd, body_len, e = struct.unpack("<IIII", hdr_data)

                # 2. 바디 읽기
                body = b""
                if body_len > 0:
                    body = await self.Reader.readexactly(body_len)

                # 3. 자동 객체 변환 및 모든 콜백 호출
                if self.Unmarshaler:
                    msg = self.Unmarshaler(cmd, body)
                    if msg:
                        for cb in self.OnRecvCallbacks:
                            if asyncio.iscoroutinefunction(cb): await cb(self, msg)
                            else: cb(self, msg)
        except Exception as e:
            if self._Running:
                logger.warn(f"[TCP] 연결 종료: {e}")
                await self.Close()

    async def Close(self):
        self._Running = False
        if self.Writer:
            self.Writer.close()
            await self.Writer.wait_closed()
        logger.info("[TCP] 세션 종료")
