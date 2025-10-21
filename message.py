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

def sendbin(conn, status, message):
    assert status in statuses, f'unrecognized status: {status}'
    conn.send(struct.pack('<BI', statustocode(status), len(message)) + message)

def recvbin(conn):
    data = ''
    while True:
        data += conn.recv(config.chunksize)
        if len(data) >= struct.calcsize('<BI'):
            code,datalen = struct.unpack_from('<BI', data)
            if len(data) >= datalen + struct.calcsize('<BI'):
                break
    code,datalen = struct.unpack_from('<BI', data)
    return codetostatus(code), data[struct.calcsize('<BI'):struct.calcsize('<BI') + datalen]

def send(conn, status, message):
    sendbin(conn, status, message.encode(config.encoding)

def recv(conn):
    status,data = recvbin(conn)
    return status, data.decode(config.encoding)
