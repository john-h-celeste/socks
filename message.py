import config

def send(conn, status, message):
    conn.send((status + '@' + message + '\0').encode(config.encoding))

def recv(conn):
    data = ''
    while not data.endswith('\0'):
        data += conn.recv(config.chunksize).decode(config.encoding)
    return data[:-1].split('@', maxsplit = 1)