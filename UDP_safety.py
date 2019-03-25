import socket

MODULE_NAME = "safety"

UDP_IP = "127.0.0.1"
UDP_PORT = 62021
UDP_TO_PORT = 62022

sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
# release right after program finishes
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("Starting - {}".format(MODULE_NAME))
while True:
    # data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    # print("[{}]".format(MODULE_NAME), "R", data.decode())
    msg = str(float(input("[{}] <<< ".format(MODULE_NAME))))
    sock.sendto(msg.encode(), (UDP_IP, UDP_TO_PORT))
    print("[{}]".format(MODULE_NAME), "S", msg)