#!/usr/bin/env python3
import socket
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python tcp_file_client.py <path_to_file> [server_ip]")
    sys.exit(1)

file_path = sys.argv[1]
server_ip = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
PORT = 5002
BUFFER_SIZE = 4096

if not os.path.isfile(file_path):
    print("File does not exist:", file_path)
    sys.exit(1)

filesize = os.path.getsize(file_path)
filename = os.path.basename(file_path)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server_ip, PORT))
    print(f"Connected to {server_ip}:{PORT}")
    header = f"FILENAME:{filename}|SIZE:{filesize}\n"
    s.sendall(header.encode('utf-8'))

    # send file in chunks
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(BUFFER_SIZE)
            if not chunk:
                break
            s.sendall(chunk)
    # wait for server confirmation
    resp = s.recv(1024)
    print("Server response:", resp.decode('utf-8').strip())
