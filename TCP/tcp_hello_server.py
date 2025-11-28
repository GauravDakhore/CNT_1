#!/usr/bin/env python3
import socket

HOST = '0.0.0.0'   # listen on all interfaces; use '127.0.0.1' for local-only
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Hello server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(1024)
            if not data:
                print("No data received. Closing.")
                continue
            msg = data.decode('utf-8').strip()
            print("Received from client:", msg)
            # reply
            reply = f"Hello, client! I got your message: '{msg}'"
            conn.sendall(reply.encode('utf-8'))
            print("Reply sent. Connection closed.")
