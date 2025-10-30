import struct

import config

statuses = [
    'OK', 'ERR', 'END',
    'AUTH', 'CRED', # authentication
    'UPLOAD', 'DOWNLOAD', 'MKDIR', 'RM', 'DIR', # filesystem operations
    'DATA', 'ACK', # file data
]

def statustocode(s):
    return statuses.index(s)

def codetostatus(c):
    return statuses[c]

class Message:
    def __init__(self, status, data):
        self.status = status
        self.data = data
    
    @property
    def text(self):
        return self.data.decode(config.encoding)

class MessageConnection:
    def __init__(self, conn):
        self.conn = conn
        self.buffer = b''

    def send(self, status, message):
        if isinstance(message, str):
            message = message.encode(config.encoding)
        assert status in statuses, f'unrecognized status: {status}'
        self.conn.send(struct.pack('<BI', statustocode(status), len(message)) + message)

    def recv(self):
        while True:
            self.buffer += self.conn.recv(config.chunksize)
            if len(self.buffer) >= struct.calcsize('<BI'):
                code,datalen = struct.unpack_from('<BI', self.buffer)
                if len(self.buffer) >= datalen + struct.calcsize('<BI'):
                    break
        code,datalen = struct.unpack_from('<BI', self.buffer)
        data,self.buffer = self.buffer[struct.calcsize('<BI'):struct.calcsize('<BI') + datalen], self.buffer[struct.calcsize('<BI') + datalen:]
        return Message(codetostatus(code), data)
    
    def close(self):
        self.conn.close()
