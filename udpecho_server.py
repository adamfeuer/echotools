#!/usr/bin/env python

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 5472)
print(f"starting up on {server_address[0]} port {server_address[1]}", file=sys.stderr)
sock.bind(server_address)


while True:
    print('\nwaiting to receive message', file=sys.stderr)
    data, address = sock.recvfrom(4096)
    
    print(f"received {len(data)} bytes from {address}")
    print(f"{data}")
    
    if data:
        sent = sock.sendto(data, address)
        print(f"sent {sent} bytes to {address}")




