#!/usr/bin/env python3
import socket

HOST = '127.0.0.1'  # server IP (use actual server IP for different machine)
PORT = 5001

message = "Hello from client!"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")
    s.sendall(message.encode('utf-8'))
    data = s.recv(4096)
    print("Received from server:", data.decode('utf-8'))
