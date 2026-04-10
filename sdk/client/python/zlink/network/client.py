# ZLink 통합 클라이언트 엔진 - v1.3 (Organic Session Learning)
import asyncio
import logging
from .tcp_client import _TcpClient, Pack
from .udp_client import _UdpClient

logger = logging.getLogger("zlink")

class Client:
    """
    ZLink 통합 네트워크 클라이언트 엔진입니다.
    수신되는 모든 패킷(TCP/UDP)의 헤더에서 SessionID를 학습하여 유기적으로 통합 관리합니다.
    """
    def __init__(self):
        self.tcp = None
        self.udp = None
        
        # 엔진 통합 세션 ID (0이면 서버에 신규 요청)
        self.session_id = 0
        
        # 엔진 통합 인터페이스
        self._unmarshaler = None
        self._packer = None
        self._on_recv_callbacks = []

    def set_protocol(self, unmarshaler, packer):
        """서버 엔진과 동일한 프로토콜 주입 인터페이스입니다."""
        self._unmarshaler = unmarshaler
        self._packer = packer

    def SetProtocol(self, unmarshaler, packer):
        self.set_protocol(unmarshaler, packer)

    def add_recv_callback(self, callback):
        """메시지 수신 시 호출될 비즈니스 콜백을 등록합니다."""
        self._on_recv_callbacks.append(callback)

    def AddRecvCallback(self, callback):
        self.add_recv_callback(callback)

    async def start(self, host, tcp_port=None, udp_port=None):
        """엔진을 활성화합니다. 시작 시 세션 ID를 초기화합니다."""
        self.session_id = 0
        success = False
        
        if tcp_port:
            self.tcp = _TcpClient(host, tcp_port)
            self.tcp.set_unmarshaler(self._handle_receive)
            if await self.tcp.start():
                success = True

        if udp_port:
            self.udp = _UdpClient(host, udp_port)
            self.udp.set_unmarshaler(self._handle_receive)
            if await self.udp.start():
                success = True
        
        return success

    async def send(self, msg, use_udp=False):
        """객체를 자동으로 패킹하여 전송합니다. TCP는 0(신규/매칭), UDP는 할당된 ID를 사용합니다."""
        if not self._packer:
            logger.error("패커(Packer)가 설정되지 않았습니다.")
            return

        # TCP는 항상 0으로 보내어 서버가 IP 매칭 또는 신규 생성을 결정하게 함
        # UDP는 할당받은 session_id를 사용하여 서버가 기존 세션을 즉시 식별하게 함
        sid_to_send = self.session_id if use_udp else 0
        data = self._packer(msg, use_udp, sid_to_send)

        if use_udp and self.udp:
            await self.udp.send(data)
        elif self.tcp:
            await self.tcp.send(data)

    def _handle_receive(self, command, body, header_session_id=0):
        """트랜스포트 계층에서 올라온 데이터를 객체로 변환하여 배포합니다."""
        # [유기적 학습] 수신 헤더에 유효한 SessionID가 있다면 내 ID로 저장
        if header_session_id > 0 and self.session_id != header_session_id:
            self.session_id = header_session_id
            logger.debug(f"[Engine] 세션 ID 학습 완료: {self.session_id}")

        if not self._unmarshaler:
            return None

        msg = self._unmarshaler(command, body)
        if msg:
            for cb in self._on_recv_callbacks:
                try:
                    result = cb(self, msg)
                    if asyncio.iscoroutine(result):
                        asyncio.ensure_future(result)
                except Exception as e:
                    logger.error(f"콜백 처리 오류: {e}")
        return msg

    async def stop(self):
        """모든 네트워크 서비스를 중단하고 세션을 초기화합니다."""
        if self.tcp: await self.tcp.stop()
        if self.udp: await self.udp.stop()
        self.session_id = 0
        logger.info("통합 클라이언트 엔진 종료 및 세션 초기화")
