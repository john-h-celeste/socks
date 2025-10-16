import socket

import clientconfig as config
import message

serverhost = input('What is the server\'s hostname?\n> ')

serverhost = 'localhost'
address = (serverhost, config.port)

def main():
    conn = socket.socket()
    conn.connect(address)
    while True:
        status,data = message.recv(conn)
        print(status, repr(data))
        break
    
    conn.close()

main()