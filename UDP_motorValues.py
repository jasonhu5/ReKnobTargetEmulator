import socket
import json
import keyboard
import time
from reprint import output
import os

MODULE_NAME = "motorValues"

UDP_IP = "127.0.0.1"
UDP_PORT = 62019
UDP_TO_PORT = 62020

# p_l_range = (4, 47)
# p_r_range = (-56, 12)
p_l_range = (0, 50)
p_r_range = (-90, 90)

state = {
    "positionLinear": 20.0, 
    "positionRotatory": 0.0, 
    "velocityLinear": 0.0, 
    "velocityRotatory": 0.0
}

sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
# release right after program finishes
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("Starting - {}".format(MODULE_NAME))
with output(initial_len=len(state)+1, interval=0) as output_lines:
    while True:
        if keyboard.is_pressed('up'):  
            if state['positionLinear'] <= p_l_range[1]:
                state['positionLinear'] += 1
        elif keyboard.is_pressed('down'):
            if state['positionLinear'] >= p_l_range[0]:
                state['positionLinear'] -= 1
        elif keyboard.is_pressed('left'):
            if state['positionRotatory'] >= p_r_range[0]:
                state['positionRotatory'] -= 1
        elif keyboard.is_pressed('right'):
            if state['positionRotatory'] <= p_r_range[1]:
                state['positionRotatory'] += 1
        else:
            pass
        time.sleep(0.03)
        # msg = input("[{}] <<< ".format(MODULE_NAME))
        # sock.sendto(msg.encode(), (UDP_IP, UDP_TO_PORT))
        sock.sendto(json.dumps(state).encode(), (UDP_IP, UDP_TO_PORT))
        # on Windows machines
        if os.name == 'nt':
            print(state["positionLinear"], state["positionRotatory"])
        # on Linux/Unix machines
        else:
            lines = json.dumps(state, indent=2).split('\n')
            output_lines[0] = "[{}] S".format(MODULE_NAME)
            i = 1
            for k, v in state.items():
                output_lines[i] = "\t{}: \t{}".format(k, v)
                i += 1
