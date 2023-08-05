import struct
from zybats.ext.communi.socketUtil import socketClient
import socket
"""
C结构体如下：
typedef struct defaultProtocolHead {
		int m_cFlag;
		int m_iLength;
		char m_pBody[];
	}DEFAULT_PROTOCOL_HEAD_S;
"""
DEFAULT_PROTOCOL_FLAG = 0xe8
class advertSocketClient(socketClient):
	# 构造函数，初始化连接
	def __init__(self, host, port):
		socketClient.__init__(self, host, port)
		self.packetHead = DEFAULT_PROTOCOL_FLAG


	# 析构函数，断开连接
	def __del__(self):
		pass

	def send_message(self, pb_binary_str):
		format_str = "<iI" + str(len(pb_binary_str)) + "s"
		ss = struct.pack(format_str, self.packetHead, socket.htonl(len(pb_binary_str)), data)
		print(ss)
		socketClient.send_data(self, ss, True)
"""
Demo:
    向BAP index发送查询PB，先构造查询PB
    调用socket发送PB数据
def build_request_index_data():
	index_request = adindex.IndexMatchRequest()
	index_request.isDebug = True
	index_request.pvid = "3584793e-f777-49d6-b964-wsx8111f8234"

	positionInfo = index_request.positionInfo
	positionInfo.psid = 263
	positionInfo.sellMode.append(1)
	positionInfo.templateId.append(10002)

	target = index_request.targets.add()
	target.categoryCode =  "110113"
	target.selectionCode.append("1101130201")

	target1 = index_request.targets.add()
	target1.categoryCode =  "101107"
	target1.selectionCode.append("1011070009")

	target2 = index_request.targets.add()
	target2.categoryCode =  "101108"
	target2.selectionCode.append("1011080001")

	target3 = index_request.targets.add()
	target3.categoryCode =  "101103"
	target3.selectionCode.append("1011030001")

	target4 = index_request.targets.add()
	target4.categoryCode =  "101105"
	target4.selectionCode.append("1011050001")

	return index_request.SerializePartialToString()


if __name__ == '__main__':
	host = "192.168.240.198"
	port = 8222
	client = advertSocketClient(host, port)
	data = build_request_index_data()
	client.send_message(data)

"""
