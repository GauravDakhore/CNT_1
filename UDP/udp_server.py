#!/usr/bin/env python3
import socket
import math

HOST = "0.0.0.0"   # listen on all interfaces
PORT = 12000       # pick a port

def handle_request(msg, addr, sock):
    msg = msg.strip()
    if not msg:
        return

    parts = msg.split()
    cmd = parts[0].upper()

    if cmd == "HELLO":
        reply = f"Hello from UDP server at {HOST}:{PORT}"
    elif cmd == "TRIG":
        # expected format: TRIG <func> <angle> <unit>
        # e.g. "TRIG sin 30 deg" or "TRIG cos 0.785 rad"
        if len(parts) < 4:
            reply = "ERROR: TRIG usage -> TRIG <sin|cos|tan> <angle> <deg|rad>"
        else:
            func = parts[1].lower()
            try:
                angle = float(parts[2])
                unit = parts[3].lower()
                if unit not in ("deg", "rad"):
                    raise ValueError("unit must be 'deg' or 'rad'")
                # convert to radians if necessary
                if unit == "deg":
                    angle_rad = math.radians(angle)
                else:
                    angle_rad = angle

                if func == "sin":
                    res = math.sin(angle_rad)
                elif func == "cos":
                    res = math.cos(angle_rad)
                elif func == "tan":
                    res = math.tan(angle_rad)
                else:
                    reply = "ERROR: function must be sin, cos, or tan"
                    sock.sendto(reply.encode(), addr)
                    return

                # format result
                reply = f"OK {func}({angle} {unit}) = {res:.6f}"
            except ValueError as ve:
                reply = "ERROR: " + str(ve)
            except Exception as e:
                reply = "ERROR: " + str(e)
    else:
        reply = "ERROR: Unknown command. Use HELLO or TRIG"

    sock.sendto(reply.encode(), addr)


def main():
    print(f"Starting UDP server on port {PORT} ...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        while True:
            data, addr = s.recvfrom(1024)
            msg = data.decode()
            print(f"Received from {addr}: {msg}")
            handle_request(msg, addr, s)


if __name__ == "__main__":
    main()
