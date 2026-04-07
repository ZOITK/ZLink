namespace Zoit.Network
{
    /// <summary>
    /// 네트워크를 통해 수신된 패킷 데이터의 공통 구조체
    /// </summary>
    public struct NetworkPacket
    {
        public uint Command; // 커맨드 ID
        public byte[] Body;  // 직렬화된 데이터 (Body)
        public uint Error;   // 에러 코드
        public uint Sender;  // 보낸 사람 (UDP용)

        public NetworkPacket(uint command, byte[] body, uint error = 0, uint sender = 0)
        {
            Command = command;
            Body = body;
            Error = error;
            Sender = sender;
        }
    }
}
