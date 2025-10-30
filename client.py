import socket

import clientconfig as config
import message

serverhost = input('What is the server\'s hostname?\n> ')

serverhost = 'localhost'
address = (serverhost, config.port)

class Client:
    def __init__(self, address, credentials):
        s = socket.socket()
        s.connect(address)
        self.conn = message.MessageConnection(s)
        pass # need to implement authentication
    
    def upload(self, filename):
        # send an UPLOAD(filename) message
        # based on response
        #   ERR: prompt overwrite y/n?
        #   OK: upload the file as a bunch of DATA messages
        pass
    
    def download(self, filename):
        # send DOWNLOAD(filename) message
        # based on response
        #   ERR: oh :(
        #   OK: take a bunch of DATA messages
        pass
    
    def delete(self, filename):
        # send DELETE(filename)
        # based on response
        #   ERR: oh :(
        #   OK: ok :)
        pass
    
    def dirs(self):
        # send DIR
        # recieve OK(files and dirs)
        pass
    
    def subfolder_create(self, path):
        # send MKDIR(path)
        # based on response
        #   ERR: oh :(
        #   OK: ok :)
        pass
    
    def subfolder_delete(self, path):
        # send RMDIR(path)
        # based on response
        #   ERR: oh :(
        #   OK: ok :)
        pass

def main():
    conn = socket.socket()
    conn.connect(address)
    conn = message.MessageConnection(conn)
    while True:
        m = conn.recvstr()
        print(m.status, repr(m.data))
        conn.sendstr('OK', input())
        break
    
    conn.close()

main()