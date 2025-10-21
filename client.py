import socket

import clientconfig as config
import message

serverhost = input('What is the server\'s hostname?\n> ')

serverhost = 'localhost'
address = (serverhost, config.port)

def main():
    conn = socket.socket()
    conn.connect(address)
    conn = message.MessageConnection(conn)
    while True:
        status,data = conn.recv()
        print(status, repr(data))
        conn.send('OK', input())
        break
    
    conn.close()

main()