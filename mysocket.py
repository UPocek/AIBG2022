import sys

_, PLAYER_NUM, TEAM_NAME = sys.argv
PLAYER_NUM = int(PLAYER_NUM)

# PLAYER_NUM = 1
# TEAM_NAME = 'TEAM 1'
AMOUNT_OF_GAMES = 10
RESTART = True
RESTART_TURN = 99

PLAYER_1_WAIT = 1
PLAYER_2_WAIT = 3

import socket
import time
import os
from bot_input import *
from receive_DTO import *
exec(open(os.getcwd() + "\\receive_DTO.py").read())
print('running ' + os.getcwd() + "\\receive_DTO.py")
exec(open(os.getcwd() + "\\send_DTO.py").read())
print('running ' + os.getcwd() + "\\send_DTO.py")
exec(open(os.getcwd() + "\\bot_input.py").read())
print('running ' + os.getcwd() + "\\bot_input.py")

#### Socket
FORMAT = 'utf-8 '
PORT_PLAYER_1 = 8081
PORT_PLAYER_2 = 8082
SERVER = '127.0.0.1'


class client_socket:
    def __init__(self,server_ip,server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.addr = (server_ip,server_port)
        self.start_connection()
        
    def send(self,msg):
        msg = bytes(msg,FORMAT)
        self.client.send(msg)
        return

    def receive(self):
        for game in range(0,AMOUNT_OF_GAMES):
            self.start_playing(game)
        self.client.close()
        
    def start_playing(self,game):
        botMsg = bot_input(self.dto)
        self.send(botMsg)
        turn = 2
        while(turn < RESTART_TURN + 1):
            if (PLAYER_NUM != 2 or turn != RESTART_TURN):
                self.get_DTO_message()
                
            is_last_game = game == AMOUNT_OF_GAMES - 1
            if (RESTART and turn == RESTART_TURN and is_last_game==False):
                    if (PLAYER_NUM == 1):
                        self.send("restart")
                    print('Restarting...')
                    self.attempt_reconnect()
            else:
                botMsg = bot_input(self.dto)
                self.send(botMsg)
            turn+=1
          
    def get_DTO_message(self):
        try:
            msg = self.client.recv(8)
            msg = msg.decode(FORMAT)
            msg = self.client.recv(int(msg))
            self.dto = DTO.from_json(msg)
        except:
            print('Exception message: ' + msg)
            time.sleep(0.2)
            self.get_DTO_message()
        return self.dto
                
    def get_first_dto(self):
        try:
            msg = self.client.recv(8)
            msg = msg.decode(FORMAT)
            msg = self.client.recv(int(msg))
            self.dto = DTO.from_json(msg)
        except:
            self.set_team_name()
                
    def set_team_name(self):
        self.send(TEAM_NAME)
        self.get_first_dto()
        
    def start_connection(self):
        time.sleep(1)
        print('Creating socket')
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Connecting to localhost')
            self.client.connect(self.addr)
            print('setting team name')
            self.set_team_name()
        except: 
            self.start_connection()
        
    def attempt_reconnect(self):
        self.client.close()
        if(PLAYER_NUM == 1):
            time.sleep(PLAYER_1_WAIT)
        else:
            time.sleep(PLAYER_2_WAIT)
        self.start_connection()
def selectPlayer():
    if(PLAYER_NUM == 1):
        return client_socket(SERVER,PORT_PLAYER_1)
    else:
        return client_socket(SERVER,PORT_PLAYER_2)
client = selectPlayer()
client.receive()