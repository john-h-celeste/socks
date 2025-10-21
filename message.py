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

    def sendbin(status, message):
        assert status in statuses, f'unrecognized status: {status}'
        self.conn.send(struct.pack('<BI', statustocode(status), len(message)) + message)

    def recvbin():
        data = ''
        while True:
            data += self.conn.recv(config.chunksize)
            if len(data) >= struct.calcsize('<BI'):
                code,datalen = struct.unpack_from('<BI', data)
                if len(data) >= datalen + struct.calcsize('<BI'):
                    break
        code,datalen = struct.unpack_from('<BI', data)
        return codetostatus(code), data[struct.calcsize('<BI'):struct.calcsize('<BI') + datalen]

    def send(status, message):
        sendbin(self.conn, status, message.encode(config.encoding)

    def recv():
        status,data = recvbin(self.conn)
        return status, data.decode(config.encoding)
