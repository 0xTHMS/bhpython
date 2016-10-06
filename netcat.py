import sys
import socket
import getopt
import threading
import subprocess

# define some global vars
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    print "BlackHat Python Programming Book - replacing netcat!"
    print "Usage: bhnet.py -t target_host -p port"
    print "-l --listen   - listen on [host]:[port] for incoming connections"
    sys.exit(0)



def server_loop():
    global target
    if not len(target)
        """ Listens on all interfaces """
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()


def run_command(command):
    """
    :param command: (string) input command-line
    :return: (string) output command-line
    """
    # trim newline
    command = command.rstrip()
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to exec command with subprocess pymodule.\r\n"

    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_destination):
        file_buffer = ""

        # keep reading until none is available
        while True:
            answer = client_socket.recv()




def client_sender(buffer):
    global target, port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to the client
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)
        while True:

            # waiting for reply
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
            print response,

            buffer = raw_input("")
            buffer += "\n"
            client.send(buffer)

    except:
        print "[*] Exception ! Exiting !"
        # tear down connection
        client.close()




def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # handle command line args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print "An error occured" + str(err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled option"

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)

    # Let's first handle listen and execute
    if listen:
        server_loop()


main()

