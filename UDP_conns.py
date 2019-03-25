import socket
import threading
import json

# default configs
UDP_IP = "127.0.0.1"

CONN_PORT = 62011
CONN_TO_PORT = 62012

MODE_PORT = 62013
MODE_TO_PORT = 62014

M_DATA_PORT = 62015
M_DATA_TO_PORT = 62016

CALI_PORT = 62017
CALI_TO_PORT = 62018

# M_VAL_PORT = 62019
# M_VAL_TO_PORT = 62020

# SAFE_PORT = 62021
# SAFE_TO_PORT = 62022

CURR_MODE = 0 
# _LOCK_CURR_MODE = threading.Lock()

def connection(
    my_port, 
    conn_port,
    my_ip=UDP_IP, 
    conn_ip=UDP_IP
): 
    global CURR_MODE
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((my_ip, my_port))
    # release right after program finishes
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Starting -", threading.currentThread().getName())
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("[{}]".format(threading.currentThread().getName()), "R", data.decode())
        msg = str(float(CURR_MODE))
        sock.sendto(msg.encode(), (conn_ip, conn_port))
        print("[{}]".format(threading.currentThread().getName()), "S", msg)

def mode(
    my_port, 
    conn_port,
    my_ip=UDP_IP, 
    conn_ip=UDP_IP
): 
    global CURR_MODE
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((my_ip, my_port))
    # release right after program finishes
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Starting -", threading.currentThread().getName())
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("[{}]".format(threading.currentThread().getName()), "R", data.decode())
        # _LOCK_CURR_MODE.acquire()
        CURR_MODE = float(data)
        msg = str(float(CURR_MODE))
        sock.sendto(msg.encode(), (conn_ip, conn_port))
        # _LOCK_CURR_MODE.release()
        print("[{}]".format(threading.currentThread().getName()), "S", msg)
  
# def input_val(
#     my_port, 
#     conn_port,
#     my_ip=UDP_IP, 
#     conn_ip=UDP_IP
# ): 
#     sock = socket.socket(socket.AF_INET, # Internet
#                         socket.SOCK_DGRAM) # UDP
#     sock.bind((my_ip, my_port))
#     # release right after program finishes
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#     print("Starting - ", threading.currentThread().getName())
#     while True:
#         msg = input(">>> input for [{}]".format(threading.currentThread().getName())) 
#         sock.sendto(msg.encode(), (conn_ip, conn_port))
#         print("[{}]".format(threading.currentThread().getName()), "S", msg)

def motor_data(
    my_port, 
    conn_port,
    my_ip=UDP_IP, 
    conn_ip=UDP_IP
): 
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((my_ip, my_port))
    # release right after program finishes
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Starting - ", threading.currentThread().getName())
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("[{}]".format(threading.currentThread().getName()), "R", data.decode())
  
def calibration(
    my_port, 
    conn_port,
    my_ip=UDP_IP, 
    conn_ip=UDP_IP
): 
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((my_ip, my_port))
    # release right after program finishes
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Starting -", threading.currentThread().getName())
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("[{}]".format(threading.currentThread().getName()), "R", data.decode())
        msg = str(float(json.loads(data)['value']))
        sock.sendto(msg.encode(), (conn_ip, conn_port))
        print("[{}]".format(threading.currentThread().getName()), "S", msg)

t_connection = threading.Thread(
    name="connection", 
    target=connection,
    args=(CONN_PORT, CONN_TO_PORT),
) 
t_mode = threading.Thread(
    name="mode", 
    target=mode,
    args=(MODE_PORT, MODE_TO_PORT),
) 
t_motor_data = threading.Thread(
    name="motorData", 
    target=motor_data,
    args=(M_DATA_PORT, M_DATA_TO_PORT),
) 
t_calibration = threading.Thread(
    name="calibration", 
    target=calibration,
    args=(CALI_PORT, CALI_TO_PORT),
) 
# t_motor_values = threading.Thread(
#     name="motorValues", 
#     target=input_val,
#     args=(M_VAL_PORT, M_VAL_TO_PORT),
# ) 
# t_safety = threading.Thread(
#     name="safety", 
#     target=input_val,
#     args=(SAFE_PORT, SAFE_TO_PORT),
# ) 

t_connection.start()
t_mode.start() 
t_motor_data.start()
t_calibration.start()
# t_motor_values.start()
# t_safety.start()
