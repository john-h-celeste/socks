import socket

import clientconfig as config
import message

serverhost = input('What is the server\'s hostname?\n> ')

serverhost = 'localhost'
address = (serverhost, config.port)

class Client:
    def __init__(self, s, credentials):
        self.conn = message.MessageConnection(s)
        pass # need to implement authentication
    
    def upload(self, filename):
        # send UPLOAD(filename)
        # if recieve ERR:
        #   prompt the user to overwrite
        #   if so:
        #     send OK
        #   else:
        #     send ERR
        #     end
        # send DATA messages from the file
        # send an END message
        pass
    
    def download(self, filename):
        # send DOWNLOAD(filename)
        # if recieve ERR:
        #   end
        # recieve DATA messages into the file until an END message is recieved
        pass
    
    def delete(self, filename):
        # send RM(filename)
        # wait for ERR or OK
        pass
    
    def dirs(self):
        # send DIR
        # recieve OK(files and dirs)
        pass
    
    def subfolder_create(self, path):
        # send MKDIR(path)
        # wait for ERR or OK
        pass
    
    def subfolder_delete(self, path):
        # send RMDIR(path)
        # wait for ERR or OK
        pass

def main():
    s = socket.socket()
    s.connect(address)
    #client = Client(s)
    conn = message.MessageConnection(s)
    while True:
        m = conn.recv()
        print(m.status, repr(m.text))
        conn.send('OK', input())
        break
    
    conn.close()

main()