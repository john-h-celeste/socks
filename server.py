import sys
import socket
import threading
import time
import os

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
        elif message.status == 'DOWNLOAD':
            self.handle_download(message.text)
        elif message.status == 'RM':
            self.handle_delete(message.text)
        elif message.status == 'DIR':
            self.handle_dirs()
        elif message.status == 'MKDIR':
            self.handle_subfolder_create(message.text)
        elif message.status == 'RMDIR':
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
        if os.path.exists(os.path.join(config.filepath, filename)):
            self.conn.send('ERR', f'File exists: {filename}')
            confirm = self.conn.recv()
            if confirm.status != 'OK':
                return
        else:
            self.conn.send('OK', f'Creating file: {filename}')
        with open(os.path.join(config.filepath, filename), 'wb') as file:
            while (msg := self.conn.recv()).status == 'DATA':
                file.write(msg.data)
        # idk just assume the message is END
    
    def handle_download(self, filename):
        # if filename does not exist:
        #   send ERR
        #   end
        # send DATA messages from the file
        # send an END message
        if not os.path.exists(os.path.join(config.filepath, filename)):
            self.conn.send('ERR', 'File does not exist: {filename}')
        else:
            self.conn.send('OK', 'ok')
        with open(os.path.join(config.filepath, filename), 'rb') as file:
            while len(chunk := file.read(config.filechunksize)) > 0:
                self.conn.send('DATA', chunk)
        self.conn.send('END', 'end')
    
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
    
    def close(self):
        self.conn.close()

def handle(s, addr):
    server = Server(s)
    print(f'connection from {addr}')
    m = server.conn.recv()
    print(m.status, m.text)
    server.handle_message(m)
    m = server.conn.recv()
    print(m.status, m.text)
    server.handle_message(m)
    server.close()
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