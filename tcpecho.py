#!/usr/bin/env python

# tcpecho commandline client
# useful for debugging tcp connection or bandwidth problems

import socket
import sys
import argparse
import random
import string
import time

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--message-size", help="message size in bytes (default: %(default)s)",
                    type=int, default=800)
    parser.add_argument("-n", "--number-of-messages", help="number of messages (default: %(default)s)",
                    type=int, default=1)
    parser.add_argument("-r", "--receive-size", help="number of bytes to receive at once (default: %(default)s)",
                    type=int, default=64)
    parser.add_argument("-d", "--delay", help="number of milliseconds to delay between sends (default: %(default)s)",
                    type=int, default=0)
    parser.add_argument("host", help="name or IP address of host to contact",
                    type=str, default=64)
    parser.add_argument("-p", "--port", help="port to contact (default: %(default)s)",
                    type=int, default=80)
    parser.add_argument("-v", "--verbose", help="verbose mode (prints packet received indicator dots)",
                    action="store_true")
    args = parser.parse_args()
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    messages = args.number_of_messages
    message_size = args.message_size
    receive_size = args.receive_size
    delay = args.delay / 1000.0
    verbose = args.verbose
    host = args.host
    port = args.port

    # Connect the socket to the port where the server is listening
    server_address = (host, port)
    print('connecting to %s port %s' % server_address, file=sys.stderr)
    sock.connect(server_address)

    try:
        # Send data
        for i in range(0, messages):
            message = bytes (''.join([random.choice(string.ascii_letters + string.digits) for n in range(message_size)]), encoding='utf-8')
            print(f'{i}: message_size: {message_size}', file=sys.stderr)

            sock.sendall(message)

            # Look for the response
            amount_received = 0
            amount_expected = len(message)
            
            print(f'receiving', file=sys.stderr, end='')
            sys.stderr.flush()

            received_packets = 0
            received_data = bytes("", encoding='utf-8')
            while amount_received < amount_expected:
                data = sock.recv(receive_size)
                received_data += data
                amount_received += len(data)
                if verbose:
                    print('.', file=sys.stderr, end='')
                    sys.stderr.flush()
                received_packets += 1
            print(f' :{received_packets}', file=sys.stderr)
            if amount_expected != amount_received:
                print(f'*** Did not receive the right number of bytes! Should have gotten {amount_expected}, but got {amount_received}.', file=sys.stderr)
            if message != received_data: 
                print(f'*** Did not receive the correct data!', file=sys.stderr)
                print(f'expected: {message}')
                print(f'received: {received_data}')
            sys.stderr.flush()
            time.sleep(delay)

    finally:
        print('closing socket', file=sys.stderr)
        sock.close()


if __name__ == "__main__":
    main()

