import time
import socket

# SENDERIP = '10.80.5.232'
# 这里应该是接收端的本地ip
RECEIVERIP = '10.80.5.232'

# 组播地址和端口。
MYPORT = 1234
MYGROUP = '224.1.1.1'


def receiver():
    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # allow multiple sockets to use the same PORT number
    # 端口复用，同1个ip上可运行多个接收端。java貌似不需要配置，默认可复用
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind to the port that we know will receive multicast data
    sock.bind((RECEIVERIP, MYPORT))
    # tell the kernel that we are a multicast socket
    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
    # Tell the kernel that we want to add ourselves to a multicast group
    # The address for the multicast group is the third param
    status = sock.setsockopt(socket.IPPROTO_IP,
                             socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(MYGROUP) + socket.inet_aton(RECEIVERIP));

    sock.setblocking(0)
    # ts = time.time()
    while 1:
        try:
            data, addr = sock.recvfrom(2048)
        except socket.error as e:
            # print(e)
            pass
        else:
            print("Receive data!")
            print("TIME:", time.time())
            print("FROM: ", addr)
            print("DATA: ", data.decode('utf-8'))


if __name__ == "__main__":
    receiver()
