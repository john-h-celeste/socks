import sys
import socket
import threading
import time

import serverconfig as config
import message

host = '0.0.0.0' # or 'localhost'
address = (host, config.port)

class Server:
    def __init__(self, s):
        self.conn = message.MessageConnection(s)
        pass # need to implement authentication
    
    def handle_message(self, message):
        # handle a message based on its status
        if message.status == 'UPLOAD':
            self.handle_upload(message.text)
        if message.status == 'DOWNLOAD':
            self.handle_download(message.text)
        if message.status == 'RM':
            self.handle_delete(message.text)
        if message.status == 'DIR':
            self.handle_dirs()
        if message.status == 'MKDIR':
            self.handle_subfolder_create(message.text)
        if message.status == 'RMDIR':
            self.handle_subfolder_delete(message.text)
        else:
            self.conn.send('ERR', f'unrecognized status: {message.status}')
    
    def handle_upload(self, filename):
        # if filename exists:
        #   send ERR
        #   if recieve OK:
        #     continue
        #   else:
        #     end
        # recieve DATA messages into the file until an END message is recieved
        pass
    
    def handle_download(self, filename):
        # if filename does not exist:
        #   send ERR
        #   end
        # send DATA messages from the file
        # send an END message
        pass
    
    def handle_delete(self, filename):
        # if filename does not exist:
        #   send ERR
        #   end
        # delete the file
        # send OK
        pass
    
    def handle_dirs(self):
        # send OK(dirs and files)
        pass
    
    def handle_subfolder_create(self, path):
        # if path exists:
        #   send ERR
        #   end
        # create subfolder
        # send OK
        pass
    
    def handle_subfolder_delete(self, path):
        # if path does not exist:
        #   send ERR
        #   end
        # delete subfolder
        # send OK
        pass

def handle(conn, addr):
    conn = message.MessageConnection(conn)
    print(f'connection from {addr}')
    conn.send('OK', 'hi <3')
    m = conn.recv()
    print(m.status, m.text)
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