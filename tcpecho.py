#!/usr/bin/env python

import socket
import sys
import argparse

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--message-size", help="message size in bytes (default: %(default)s)",
                    type=int, default=800)
    parser.add_argument("-n", "--number-of-messages", help="number of messages (default: %(default)s)",
                    type=int, default=1)
    args = parser.parse_args()
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('10.0.0.2', 80)
    print('connecting to %s port %s' % server_address, file=sys.stderr)
    sock.connect(server_address)

    messages = args.number_of_messages
    message_size = args.message_size

    try:
        # Send data
        #message = bytes('This is the message.  It will be repeated.', encoding='utf-8')
        for i in range(0, messages):
            #message_size += 1
            message = bytes('a' * message_size, encoding='utf-8')
            print(f'{i}: message_size: {message_size}', file=sys.stderr)
            #print(f'{i}: sending "{message}"', file=sys.stderr)

            sock.sendall(message)

            # Look for the response
            amount_received = 0
            amount_expected = len(message)
            
            print(f'receiving', file=sys.stderr, end='')
            sys.stderr.flush()

            received_packets = 0
            while amount_received < amount_expected:
                data = sock.recv(16)
                amount_received += len(data)
                #print(f'received "{data}"', file=sys.stderr)
                print('.', file=sys.stderr, end='')
                sys.stderr.flush()
                received_packets += 1
            print(f' :{received_packets}', file=sys.stderr)
            sys.stderr.flush()

    finally:
        print('closing socket', file=sys.stderr)
        sock.close()


if __name__ == "__main__":
    main()

