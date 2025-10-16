import os
import socket
import threading

import serverconfig as config

host = '0.0.0.0' # or 'localhost'
address = (host, config.port)

def handle(conn, addr):
    print(f'connected at {addr}')
    conn.send('hi <3'.encode(config.encoding))
    conn.close()

def main():
    print(f'started (i am {repr(socket.gethostname())})')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(address)
    s.listen()
    
    while True:
        conn,addr = s.accept()
        thread = threading.Thread(target = handle, args = (conn, addr))
        thread.start()

main()