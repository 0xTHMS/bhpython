#!/bin/python2.7

import sys
import socket
import threading

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # connect to remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

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
