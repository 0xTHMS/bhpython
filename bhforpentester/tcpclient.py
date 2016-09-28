import socket

target_host = "0.0.0.0"
target_port = 1337

# create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect
client.connect((target_host, target_port))

client.send("DATA")
response = client.recv(4096)

print response
