import config

def send(conn, status, message):
    assert '@' not in status, 'the status may not contain an at sign (\'@\')'
    assert '\0' not in message, 'the message may not contain a null character (\'\\0\')'
    conn.send((status + '@' + message + '\0').encode(config.encoding))

def recv(conn):
    data = ''
    while not data.endswith('\0'):
        data += conn.recv(config.chunksize).decode(config.encoding)
    return data[:-1].split('@', maxsplit = 1)