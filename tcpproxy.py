#!/bin/python2.7

import sys
import socket
import threading


# this is a pretty hex dumping function directly taken from
# the comments here:
# http://code.activestate.com/recipes/142812-hex-dumper/
def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X %-*s %s" % (i, length*(digits + 1), hexa,  text))
    print b'\n'.join(result)


def receive_from(connection):
    buffer = ""

    connection.settimeout(2)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass

    return buffer


def request_handler(buffer):
    # perform packet modifications
    return buffer

def response_handler(buffer):
    # perform packet modif
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    """
    Added this for completion..
    :type client_socket: socket.socket

    """

    # connect to remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to our response handler
        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):
            print "[<==] send %d bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)

        # now lets loop and reom from local
        # send to remote, send to local
        # rinse, wash, repeat
        while True:
            # read from local host
            local_buffer = receive_from(client_socket)

            if len(local_buffer):
                print "[==>] received %d bytes from localhosts." % len(local_buffer)
                hexdump(local_buffer)

                # send it to our request handler
                local_buffer = request_handler(local_buffer)
                # send off data to the remote host
                remote_socket.send(local_buffer)
                print "[==>] Sent to remote."

            # receive back the response
            remote_buffer = receive_from(remote_socket)

            if len(remote_buffer):
                print "[<==] Received %d bytes from remote." % len(remote_buffer)
                hexdump(remote_buffer)

                # send to our response handler
                remote_buffer = response_handler(remote_buffer)

                # send the response to local socket
                client_socket.send(remote_buffer)

                print "[<==] Sent to localhost"

            # if no more dalata on either side, close connection
            if not len(remote_buffer) or not len(local_buffer):
                client_socket.close()
                remote_socket.close()
                print "[*] No more data, closing connections."

                break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listne on %s:%d" % (local_host, local_port)
        sys.exit(0)

    print "[++] Listening on %s:%d" % (local_host, local_port)

    # accept 5 connections
    server.listen(5)

    # processing requests:
    while True:
        client_socket, addr = server.accept()

        # print the local connection info
        print "[==>] Received incoming connection from %s:%d" % (addr[0], addr[1])
        proxy_thread = threading.Thread(target=proxy_handler,
                                        args=(client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()


def main():
    if len(sys.argv[1:]) != 5:
        print "[??] Usage: ./tcpproxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"
        print "Exemple: ./proxy 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # this tells our proxy to connect and receive data before sending some data
    receive_first = sys.argv[5]

    if "True" in sys.argv[5]:
        receive_first = True
    else:
        receive_first = False

    # now spinning our socket
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


main()
