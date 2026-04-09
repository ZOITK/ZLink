"""
기본 에코 클라이언트 - 간단한 메시지 송수신
"""
import asyncio
import os
import sys

# SDK 경로 추가 (sdk/client/py 하위의 zlink 폴더를 찾기 위함)
sys.path.append(os.path.join(os.path.dirname(__file__), "../../sdk/client/py"))

from zlink.network.tcp_client import AsyncTcpClient
from zlink.logger.logger import logger
import zlink.protocol.Protocol as protocol


# 클라이언트 상태 관리
class BasicClient:
	def __init__(self, nickname: str):
		"""클라이언트 초기화"""
		self.nickname = nickname
		self.player_id = None
		self.running = True

	async def login(self, client):
		"""로그인 요청 전송"""
		logger.info(f"[Client] 로그인 시도: {self.nickname}")
		req = protocol.Msg_AuthLoginReq(Nickname=self.nickname)
		await client.Send(req.BuildTCP())

	async def send_message(self, client, message: str):
		"""메시지 전송"""
		logger.info(f"[Client] 메시지 전송: {message}")
		req = protocol.Msg_MessageSendReq(Message=message)
		await client.Send(req.BuildTCP())


# 클라이언트 전역 인스턴스
basic_client = None


async def OnRecvPacket(client, msg):
	"""패킷 수신 핸들러"""
	global basic_client

	if isinstance(msg, protocol.Msg_AuthLoginRes):
		await handle_login_response(client, msg)

	elif isinstance(msg, protocol.Msg_MessageSendRes):
		await handle_send_response(msg)

	elif isinstance(msg, protocol.Msg_MessageReceiveNotify):
		await handle_receive_notify(msg)

	elif isinstance(msg, protocol.Msg_SystemTCPHeartBitRes):
		logger.debug(f"[System] 하트비트 응답: {msg.ServerTime}")


async def handle_login_response(client, msg):
	"""로그인 응답 처리"""
	global basic_client
	if msg.Result == 0:
		basic_client.player_id = msg.PlayerID
		logger.info(f"[Client] ✓ 로그인 성공 (ID: {msg.PlayerID})")

		# 메시지 전송
		await asyncio.sleep(0.5)
		await basic_client.send_message(client, "안녕하세요!")
	else:
		logger.error(f"[Client] ✗ 로그인 실패: {msg.Result}")


async def handle_send_response(msg):
	"""메시지 전송 응답"""
	if msg.Result == 0:
		logger.info("[Client] ✓ 메시지 전송 성공")


async def handle_receive_notify(msg):
	"""메시지 수신 알림"""
	logger.info(f"[Chat] {msg.Nickname}: {msg.Message}")


async def main():
	"""메인 함수"""
	global basic_client

	logger.info("🚀 기본 에코 클라이언트 시작")

	# 클라이언트 초기화
	client = AsyncTcpClient(Host="127.0.0.1", Port=8080)
	protocol.Register(client, OnRecvPacket)

	# 기본 클라이언트 생성
	import sys
	nickname = sys.argv[1] if len(sys.argv) > 1 else "Player1"
	basic_client = BasicClient(nickname)

	# 서버 연결
	logger.info(f"[Network] 서버 연결 중... (127.0.0.1:8080)")
	if not await client.Connect():
		logger.error("[Network] 서버 연결 실패")
		return

	logger.info("[Network] ✓ 서버 연결 성공")

	# 로그인
	await basic_client.login(client)

	# 하트비트 루프
	_ = asyncio.create_task(heartbeat_loop(client))

	# 10초 유지
	await asyncio.sleep(10)

	logger.info("[Network] 연결 종료")
	await client.Close()


async def heartbeat_loop(client):
	"""하트비트 전송 루프"""
	while basic_client.running:
		await asyncio.sleep(5)
		req = protocol.Msg_SystemTCPHeartBitReq(ServerTime=int(__import__('time').time() * 1000))
		try:
			await client.Send(req.BuildTCP())
		except Exception as e:
			logger.error(f"[System] 하트비트 전송 실패: {e}")
			break


if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		logger.info("사용자에 의해 중단됨")
	except Exception as e:
		logger.error(f"오류 발생: {e}")
