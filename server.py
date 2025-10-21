import sys
import socket
import threading
import time

import serverconfig as config
import message

host = '0.0.0.0' # or 'localhost'
address = (host, config.port)

def handle(conn, addr):
    conn = message.MessageConnection(conn)
    print(f'connection from {addr}')
    conn.send('OK', 'hi <3')
    print(conn.recv())
    conn.close()
    print(f'ended connection from {addr}')

def main():
    print(f'started (i am {repr(socket.gethostname())})')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(address)
    s.listen()
    
    while True:
        try:
            conn,addr = s.accept()
        except KeyboardInterrupt:
            sys.exit()
        thread = threading.Thread(target = handle, args = (conn, addr), daemon = False)
        thread.start()

threading.Thread(target = main, args = (), daemon = True).start()

try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    sys.exit()