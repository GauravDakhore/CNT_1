#!/usr/bin/env python3
import socket

SERVER_IP = "127.0.0.1"   # change to server IP if on different machine
SERVER_PORT = 12000
TIMEOUT = 3.0

def send_and_recv(message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(TIMEOUT)
        s.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
        try:
            data, _ = s.recvfrom(2048)
            return data.decode()
        except socket.timeout:
            return "No response (timeout)"

def interactive():
    print("UDP Client (HELLO / TRIG). Commands:")
    print("  HELLO")
    print("  TRIG <sin|cos|tan> <angle> <deg|rad>")
    print("  QUIT")
    while True:
        cmd = input("Enter command: ").strip()
        if not cmd:
            continue
        if cmd.upper() == "QUIT":
            break
        resp = send_and_recv(cmd)
        print("Server ->", resp)

if __name__ == "__main__":
    interactive()
