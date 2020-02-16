#!/usr/bin/env python

# udpecho commandline client
# useful for debugging IP or UDP connection or bandwidth problems

import socket
import sys
import argparse
import random
import string

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--message-size", help="message size in bytes (default: %(default)s)",
                    type=int, default=512)
    parser.add_argument("-n", "--number-of-messages", help="number of messages (default: %(default)s)",
                    type=int, default=1)
    parser.add_argument("host", help="name or IP address of host to contact",
                    type=str, default="localhost")
    parser.add_argument("-p", "--port", help="port to contact (default: %(default)s)",
                    type=int, default=80)
    parser.add_argument("-v", "--verbose", help="verbose mode (prints packet received indicator dots)",
                    action="store_true")
    args = parser.parse_args()
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    messages = args.number_of_messages
    message_size = args.message_size
    verbose = args.verbose
    host = args.host
    port = args.port

    if host == "localhost":
        host = "127.0.0.1"

    # Set up the address of the port where the server is listening
    server_address = (host, port)

    try:
        # Send data
        for i in range(0, messages):
            print('sending message to %s port %s' % server_address, file=sys.stderr)
            sequence_header = f"{i} "
            message_str = sequence_header + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(message_size - len(sequence_header))])
            message = bytes (message_str, encoding='utf-8')
            print(f'{i}: message_size: {message_size}', file=sys.stderr)

            sock.sendto(message, server_address)

            # Look for the response
            amount_received = 0
            amount_expected = len(message)
            
            print(f'receiving', file=sys.stderr, end='')
            sys.stderr.flush()

            received_packets = 0
            received_data = bytes("", encoding='utf-8')
            while amount_received < amount_expected:
                data, data_server_address = sock.recvfrom(message_size)
                received_data += data
                amount_received += len(data)
                if verbose:
                    print('.', file=sys.stderr, end='')
                    sys.stderr.flush()
                received_packets += 1
            print(f' :{received_packets}', file=sys.stderr)
            if server_address != data_server_address:
                print(f'*** Did not receive message from right server address! Should have received from {server_address}, but got {data_server_address}.', file=sys.stderr)
            if amount_expected != amount_received:
                print(f'*** Did not receive the right number of bytes! Should have gotten {amount_expected}, but got {amount_received}.', file=sys.stderr)
            if message != received_data: 
                print(f'*** Did not receive the correct data!', file=sys.stderr)
                print(f'expected: {message}')
                print(f'received: {received_data}')
            received_sequence_number = int(data.decode("utf-8").split(' ')[0])
            if i!= received_sequence_number:
                print(f'*** Did not receive the correct sequence number!', file=sys.stderr)
                print(f'expected: {i}')
                print(f'received: {received_sequence_number}')
            sys.stderr.flush()

    finally:
        print('closing socket', file=sys.stderr)
        sock.close()


if __name__ == "__main__":
    main()

