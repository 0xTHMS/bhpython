# Working UDP Server

import socket
import threading

server_ip = "0.0.0.0"
server_port = 1337

# create server object
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind on iport
server.bind((server_ip,server_port))

print "Listening on %s : %d " % (server_ip, server_port)

# Client handler fonction
def handle_client(client_socket):
    print "Enterend handle clent"
    # receive requests
    request = client_socket.recv(1024)
    print "Received %S from " % request


while True:
    test = server.recv(2024)
    print "got connection %s " % test

