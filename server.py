import sys
import socket
import threading

import serverconfig as config
import message

host = '0.0.0.0' # or 'localhost'
address = (host, config.port)

def handle(conn, addr):
    conn = message.MessageConnection(conn)
    print(f'connected at {addr}')
    conn.send('OK', 'hi <3')
    conn.close()

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
        thread = threading.Thread(target = handle, args = (conn, addr))
        thread.start()

main()