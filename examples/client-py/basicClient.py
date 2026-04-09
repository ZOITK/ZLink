import asyncio
import time
import sys
import os

# 현재 폴더의 zlink를 패키지로 인식하도록 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from zlink.sdk.Network.tcp_client import AsyncTcpClient
from zlink.sdk.Network.udp_client import AsyncUdpClient
from zlink.sdk.logger.logger import logger
from zlink.protocol import protocol

class ExampleClient:
    def __init__(self):
        self.tcp_client = AsyncTcpClient("127.0.0.1", 8080)
        self.udp_client = None
        self.player_id = 0
        self.done = asyncio.Event()
        self.udp_echo_count = 0

    async def on_tcp_recv(self, client, msg):
        """TCP 패킷 수신 처리"""
        if isinstance(msg, protocol.Msg_AuthLoginRes):
            if msg.Result == protocol.Err_None:
                self.player_id = msg.PlayerID
                logger.info(f"[TCP] 로그인 성공! PlayerID: {self.player_id}")
                
                # 시나리오 2: "안녕하세요" 메시지 전송
                logger.info("[TCP] '안녕하세요' 메시지 전송...")
                req = protocol.Msg_MessageSendReq(Message="안녕하세요")
                await self.tcp_client.Send(req.BuildTCP())
            else:
                logger.error(f"[TCP] 로그인 실패: {msg.Result}")
                self.done.set()

        elif isinstance(msg, protocol.Msg_MessageSendRes):
            logger.info("[TCP] 메시지 전송 성공 확인 수신")
            
            # 시나리오 3: UDP 하트비트 10회 전송 시작
            asyncio.create_task(self.run_udp_scenario())

        elif isinstance(msg, protocol.Msg_MessageReceiveNotify):
            logger.info(f"[Notify] {msg.Nickname}: {msg.Message}")

    async def on_udp_recv(self, cmd, body, sender, error):
        """UDP 패킷 수신 처리 (SDK AsyncUdpClient 콜백)"""
        msg = protocol._Unmarshal(cmd, body)
        if isinstance(msg, protocol.Msg_SystemUDPHeartBitRes):
            self.udp_echo_count += 1
            logger.info(f"[UDP] 에코 응답 수신 ({self.udp_echo_count}/10), TS: {msg.Timestamp}")
            
            if self.udp_echo_count >= 10:
                # 시나리오 4: 1초 대기 후 종료
                logger.info("[Scenario] UDP 에코 테스트 완료. 1초 대기...")
                await asyncio.sleep(1)
                self.done.set()

    async def run_udp_scenario(self):
        """UDP 하트비트 10회 전송 시나리오"""
        logger.info("[UDP] 하트비트 10회 전송 시작 (0.1초 간격)")
        for i in range(1, 11):
            ts = int(time.time() * 1000)
            req = protocol.Msg_SystemUDPHeartBitReq(Timestamp=ts)
            # UDP 헤더에 PlayerID를 Sender로 포함시켜 전송
            await self.udp_client.send(protocol.Cmd_SystemUDPHeartBitReq, req.Encode(), sender_idx=self.player_id)
            logger.info(f"[UDP] 하트비트 전송 ({i}/10), TS: {ts}")
            await asyncio.sleep(0.1)

    async def run(self):
        # 1. 프로토콜 및 엔진 초기화
        protocol.Register(self.tcp_client, self.on_tcp_recv)
        
        # UDP 포트를 서버 설정(8090)과 맞춤
        self.udp_client = AsyncUdpClient("127.0.0.1", 8090, on_receive=self.on_udp_recv)

        # 2. 서버 접속
        logger.info("[Network] 서버 접속 중 (127.0.0.1:8080)")
        if not await self.tcp_client.Connect():
            logger.error("[Network] TCP 접속 실패")
            return

        if not await self.udp_client.start():
            logger.error("[Network] UDP 시작 실패")
            return

        # 3. 로그인 시도
        logger.info("[TCP] 로그인 요청 전송: ExampleUser")
        login_req = protocol.Msg_AuthLoginReq(Nickname="ExampleUser")
        await self.tcp_client.Send(login_req.BuildTCP())

        # 4. 시나리오 완료 대기
        try:
            await asyncio.wait_for(self.done.wait(), timeout=15)
        except asyncio.TimeoutError:
            logger.warning("[Timeout] 시나리오가 15초 내에 완료되지 않았습니다.")
        
        # 5. 종료
        logger.info("[Network] 연결 종료 및 예제 프로그램 종료")
        await self.tcp_client.Close()
        await self.udp_client.close()

if __name__ == "__main__":
    client = ExampleClient()
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        pass
