import struct

import config

statuses = [
    'OK', 'ERR',
    'AUTH', 'CRED', # authentication
    'UPLOAD', 'DOWNLOAD', 'MKDIR', 'RM', 'DIR', # filesystem operations
    'DATA', 'ACK', # file data
]

def statustocode(s):
    return statuses.index(s)

def codetostatus(c):
    return statuses[c]

class MessageConnection:
    def __init__(self, conn):
        self.conn = conn

    def sendbin(self, status, message):
        assert status in statuses, f'unrecognized status: {status}'
        self.conn.send(struct.pack('<BI', statustocode(status), len(message)) + message)

    def recvbin(self):
        data = b''
        while True:
            data += self.conn.recv(config.chunksize)
            if len(data) >= struct.calcsize('<BI'):
                code,datalen = struct.unpack_from('<BI', data)
                if len(data) >= datalen + struct.calcsize('<BI'):
                    break
        code,datalen = struct.unpack_from('<BI', data)
        return codetostatus(code), data[struct.calcsize('<BI'):struct.calcsize('<BI') + datalen]

    def send(self, status, message):
        self.sendbin(status, message.encode(config.encoding))

    def recv(self):
        status,data = self.recvbin()
        return status, data.decode(config.encoding)
