import asyncio
import time
from engine.network.tcp_client import AsyncTcpClient
from engine.logger.logger import logger
import protocol.Protocol as protocol

async def OnRecvPacket(Client, Msg):
    """
    [통일된 핸들러] 서버로부터 파싱된 객체를 받는 중앙 집중형 처리기
    """
    if isinstance(Msg, protocol.Msg_AuthLoginRes):
        logger.info(f"[Handler] 로그인 응답 수신: UserIdx={Msg.UserIdx}, Result={Msg.Result}")
        
    elif isinstance(Msg, protocol.Msg_SystemTCPHeartBitRes):
        logger.debug(f"[Handler] 하트비트 응답 수신: {Msg.ServerTime}")

async def main():
    logger.info("ZPP Framework Unified Python Client 시작")
    
    # 1. TCP 클라이언트 초기화
    client = AsyncTcpClient(Host="127.0.0.1", Port=8080)
    
    # 2. [통일된 사용법] Register 한 줄로 프로토콜과 핸들러 바인딩
    protocol.Register(client, OnRecvPacket)
    
    # 3. 서버 연결
    if not await client.Connect():
        return

    # 4. 로그인 요청 전송 (BuildTCP 사용으로 통일성 확보)
    logger.info("[Main] 로그인 요청 전송 시도...")
    login_req = protocol.Msg_AuthLoginReq(LoginID="unified_bot_01")
    await client.Send(login_req.BuildTCP())

    # 5. 하트비트 루프
    try:
        while True:
            await asyncio.sleep(5)
            heartbeat = protocol.Msg_SystemTCPHeartBitReq(ServerTime=time.time())
            await client.Send(heartbeat.BuildTCP())
    except asyncio.CancelledError:
        pass
    finally:
        await client.Close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
