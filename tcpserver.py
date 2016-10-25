import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 1337
nbclients = 0

# server object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind to port
server.bind((bind_ip, bind_port))
server.listen(5)

# accept
print "Listening on %s port %s" % (bind_ip, bind_port)


def handle_client(client_socket,nbclients):
    # print what client sends.
    request = client_socket.recv(1024)
    print "Received %s\r\n " % request

    client_socket.send("ACK!")
    client_socket.close()

while True:
    (client, addr) = server.accept()
    print "Accepted connection from %s on port %s" % (addr[0], addr[1])

    # thread for out client
    client_handler = threading.Thread(target=handle_client, args=(client, nbclients,))
    client_handler.start()



