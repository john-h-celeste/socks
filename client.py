import socket
import os

import clientconfig as config
import message

#serverhost = input('What is the server\'s hostname?\n> ')

serverhost = 'localhost'
address = (serverhost, config.port)

class Client:
    def __init__(self, s, credentials):
        self.conn = message.MessageConnection(s)
        pass # need to implement authentication
    
    def upload(self, file, filename):
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
        self.conn.send('UPLOAD', filename)
        resp = self.conn.recv()
        if resp.status == 'ERR':
            print('The file already exists. Do you want to overwrite it?')
            choice = input('> ')
            if choice[0].upper() == 'Y':
                self.conn.send('OK', 'yes')
                print('Confirmed.')
            else:
                self.conn.send('ERR', 'no')
                print('Aborted.')
                return
        while len(chunk := file.read(config.filechunksize)) > 0:
            self.conn.send('DATA', chunk)
        self.conn.send('END', 'end')
    
    def download(self, filename):
        # send DOWNLOAD(filename)
        # if recieve ERR:
        #   end
        # recieve DATA messages into the file until an END message is recieved
        self.conn.send('DOWNLOAD', filename)
        resp = self.conn.recv()
        if resp.status == 'ERR':
            print(resp.data)
            return
        with open(os.path.join(config.datapath, filename), 'wb') as file:
            while (msg := self.conn.recv()).status == 'DATA':
                file.write(msg.data)
        # idk just assume the message is END
    
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
    
    def close(self):
        # maybe tell the server?
        self.conn.close()

def main():
    s = socket.socket()
    s.connect(address)
    client = Client(s, '')
    with open('client.py', 'rb') as f:
        client.upload(f, 'file')
        client.download('file')
    
    client.close()

main()