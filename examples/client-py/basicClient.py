import asyncio
import time
import sys
import os

# 현재 폴더의 zlink와 protocol을 패키지로 인식하도록 경로 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zlink.network.client import Client
from zlink.logger.logger import logger
import protocol.protocol as protocol

class ExampleClient:
    def __init__(self):
        # 통합 클라이언트 엔진 - TCP/UDP를 하나의 객체로 관리
        self.client = Client()
        self.player_id = 0
        self.done = asyncio.Event()
        self.udp_echo_count = 0

    async def on_recv(self, engine, msg):
        """모든 패킷 수신 처리 (TCP/UDP 통합 콜백)"""
        if isinstance(msg, protocol.Msg_AuthLoginRes):
            if (msg.Result or 0) == protocol.Err_None:
                self.player_id = msg.PlayerID
                logger.info(f"[TCP] 로그인 성공! PlayerID: {self.player_id}")

                # 시나리오 2: 메시지 전송
                req = protocol.Msg_MessageSendReq(Message="안녕하세요")
                await self.client.send(req)

            else:
                logger.error(f"[TCP] 로그인 실패: {msg.Result}")
                self.done.set()

        elif isinstance(msg, protocol.Msg_MessageSendRes):
            logger.info("[TCP] 전송 성공 확인")
            # 시나리오 3: UDP 하트비트 10회 전송
            asyncio.create_task(self.run_udp_scenario())

        elif isinstance(msg, protocol.Msg_SystemUDPHeartBitRes):
            self.udp_echo_count += 1
            logger.info(f"[UDP] 에코 응답 수신 ({self.udp_echo_count}/10), TS: {msg.Timestamp}")
            if self.udp_echo_count >= 10:
                logger.info("[Scenario] UDP 에코 테스트 완료. 1초 대기...")
                await asyncio.sleep(1)
                self.done.set()

    async def run_udp_scenario(self):
        """UDP 하트비트 10회 전송 시나리오"""
        logger.info("[UDP] 하트비트 10회 전송 시작 (0.1초 간격)")
        for i in range(1, 11):
            ts = int(time.time() * 1000)
            req = protocol.Msg_SystemUDPHeartBitReq(Timestamp=ts)
            await self.client.send(req, use_udp=True)
            logger.info(f"[UDP] 하트비트 전송 ({i}/10), TS: {ts}")
            await asyncio.sleep(0.1)

    async def run(self):
        # 1. 통합 엔진에 프로토콜 등록 (서버와 동일한 인터페이스)
        protocol.Register(self.client, self.on_recv)

        # 2. 서버 접속 (TCP + UDP 동시 활성화)
        logger.info("[Network] 서버 접속 중 (TCP:8080 / UDP:8090)")
        if not await self.client.start("127.0.0.1", tcp_port=8080, udp_port=8090):
            logger.error("[Network] 서버 접속 실패")
            return

        # 3. 로그인 시도
        logger.info("[TCP] 로그인 요청 전송: ExampleUser")
        await self.client.send(protocol.Msg_AuthLoginReq(Nickname="ExampleUser"))

        # 4. 시나리오 완료 대기
        try:
            await asyncio.wait_for(self.done.wait(), timeout=15)
        except asyncio.TimeoutError:
            logger.warning("[Timeout] 시나리오가 15초 내에 완료되지 않았습니다.")

        # 5. 종료
        logger.info("[Network] 연결 종료")
        await self.client.stop()

if __name__ == "__main__":
    client = ExampleClient()
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        pass
