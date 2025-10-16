import os
import socket

import clientconfig as config

serverhost = input('What is the server\'s hostname?\n> ')

serverhost = 'localhost'
address = (serverhost, config.port)

def main():
    s = socket.socket()
    s.connect(address)
    while True:
        data = s.recv(config.chunksize).decode(config.encoding)
        print(data)
        break
    
    s.close()

main()