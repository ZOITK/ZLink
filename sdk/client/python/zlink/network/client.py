# ZLink 통합 클라이언트 엔진 - v1.1 (Orchestrator)
import asyncio
import logging
from .tcp_client import AsyncTcpClient, Pack
from .udp_client import AsyncUdpClient

logger = logging.getLogger("zlink")

class Client:
    """
    ZLink 통합 네트워크 클라이언트 엔진입니다.
    서버 엔진(network.Server)과 대칭되는 구조를 가지며, 
    TCP와 UDP 전송을 내부에서 통합 관리합니다.
    """
    def __init__(self):
        self.tcp = None
        self.udp = None
        
        # 엔진 통합 인터페이스
        self._unmarshaler = None
        self._packer = None
        self._on_recv_callbacks = []

    def set_protocol(self, unmarshaler, packer):
        """서버 엔진과 동일한 프로토콜 주입 인터페이스입니다."""
        self._unmarshaler = unmarshaler
        self._packer = packer
        
        # 하위 트랜스포트에도 전파 (필요시)
        if self.tcp: self.tcp.set_unmarshaler(self._handle_receive)
        if self.udp: self.udp.set_unmarshaler(self._handle_receive)

    def SetProtocol(self, unmarshaler, packer):
        """Go 정합을 위한 파스칼 케이스 알리어스"""
        self.set_protocol(unmarshaler, packer)

    def add_recv_callback(self, callback):
        """메시지 수신 시 호출될 비즈니스 콜백을 등록합니다."""
        self._on_recv_callbacks.append(callback)

    def AddRecvCallback(self, callback):
        """Go 정합을 위한 파스칼 케이스 알리어스"""
        self.add_recv_callback(callback)

    async def start(self, host, tcp_port=None, udp_port=None):
        """엔진을 활성화합니다. 필요한 포트만 지정하여 시작할 수 있습니다."""
        success = False
        
        if tcp_port:
            self.tcp = AsyncTcpClient(host, tcp_port)
            self.tcp.set_unmarshaler(self._handle_receive)
            if await self.tcp.start():
                success = True

        if udp_port:
            self.udp = AsyncUdpClient(host, udp_port)
            self.udp.set_unmarshaler(self._handle_receive)
            if await self.udp.start():
                success = True
        
        return success

    async def send(self, msg, use_udp=False):
        """객체를 자동으로 패킹하여 전송합니다. 전송 방식(TCP/UDP)을 선택할 수 있습니다."""
        if not self._packer:
            logger.error("패커(Packer)가 설정되지 않았습니다.")
            return

        # 서버로부터 할당받은 SessionID (TCP 응답 헤더에서 추출)
        session_id = self.tcp.session_id if self.tcp else 0

        # UDP 전송시 SessionID를 함께 전달하여 서버가 세션을 매칭할 수 있도록 함
        data = self._packer(msg, use_udp, session_id)

        if use_udp and self.udp:
            await self.udp.send(data)
        elif self.tcp:
            await self.tcp.send(data)

    def _handle_receive(self, command, body):
        """트랜스포트 계층에서 올라온 데이터를 객체로 변환하여 배포합니다."""
        if not self._unmarshaler:
            return None

        msg = self._unmarshaler(command, body)
        if msg:
            for cb in self._on_recv_callbacks:
                try:
                    result = cb(self, msg)
                    # async 콜백 지원
                    if asyncio.iscoroutine(result):
                        asyncio.ensure_future(result)
                except Exception as e:
                    logger.error(f"콜백 처리 오류: {e}")
        return msg

    async def stop(self):
        """모든 네트워크 서비스를 중단합니다."""
        if self.tcp: await self.tcp.stop()
        if self.udp: await self.udp.stop()
        logger.info("통합 클라이언트 엔진 종료")
