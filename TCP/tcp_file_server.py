#!/usr/bin/env python3
import socket
import os

HOST = '0.0.0.0'
PORT = 5002
BUFFER_SIZE = 4096
RECV_DIR = 'received_files'
os.makedirs(RECV_DIR, exist_ok=True)

def recv_all(conn, size):
    data = b''
    while len(data) < size:
        chunk = conn.recv(min(BUFFER_SIZE, size - len(data)))
        if not chunk:
            break
        data += chunk
    return data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"File server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        with conn:
            # read header line
            header = b''
            while not header.endswith(b'\n'):
                ch = conn.recv(1)
                if not ch:
                    break
                header += ch
            header = header.decode('utf-8').strip()
            print("Header:", header)
            # expect header like: FILENAME:example.txt|SIZE:1234
            try:
                parts = dict(part.split(':',1) for part in header.split('|'))
                filename = os.path.basename(parts['FILENAME'])
                filesize = int(parts['SIZE'])
            except Exception as e:
                print("Bad header:", e)
                conn.sendall(b"ERROR: Bad header\n")
                continue

            # receive file bytes
            print(f"Receiving file '{filename}' of {filesize} bytes")
            filedata = recv_all(conn, filesize)
            if len(filedata) != filesize:
                print(f"Warning: received {len(filedata)} bytes (expected {filesize})")
            save_path = os.path.join(RECV_DIR, filename)
            with open(save_path, 'wb') as f:
                f.write(filedata)
            print(f"Saved to {save_path}")
            conn.sendall(f"OK: Received {len(filedata)} bytes\n".encode('utf-8'))
