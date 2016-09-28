import socket

target_host = "127.0.0.1"
target_port = 1337

# create client object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send some data
client.sendto("DATA", (target_host, target_port))

data, addr = client.recv(4096)

print data
