from threading import Thread
import socket
import netutils
import queue
import time
import numpy as np
import re

clients = {}


# Main function
def main():     # called at the end of the file
    # Prepares the queue of tasks to be performed by the consumer
    q = queue.Queue()
    # Initiate the consumer program who deals with printings
    c = consumer(q)
    c.daemon = True     # NB: the program terminates when all non-daemon thread are done
    c.start()
    # Start to receive request from clients
    handle_acceptall(q).start()


# This is the server, opens the socket in order to receive requests
def handle_acceptall(q):
    def handle():
        # create a socket that listens (on a port of your choice)

        server_socket = socket.socket()
        port = 1234  # np.random.randint(1000,9999)
        server_socket.bind(('', port))
        print("socket bound to %s" % port)
        server_socket.listen()
        print("socket is listening")
        print("Server IP address: ", socket.gethostbyname(socket.gethostname()))

        while True:
            # Establish connection with client.
            socket_c, addr = server_socket.accept()
            clients[addr] = socket_c
            print('Got connection from', addr)
            # The producer will handle connections with clients
            producer(socket_c, addr, q).start()

    t = Thread(target=handle)
    return t


# Takes care of incoming messages from the client, puts them in a queue
def producer(socket, addr, q):

    # Check for timeout if peer doesn't say anything
    def handle():

        while True:
            # read two lines then ignore anything from this client...
            try:
                l = netutils.read_line(socket)
            except ConnectionResetError:
                print("Connection to a peer was forcibly closed.")
                break
            print("RECEIVED Message:", str(l))
            if l is None:
                break
            msg = l.split(" ")
            if l == "QUIT" or l == "Quit" or l == "quit" or l == "List received, Close connection":
                q.put((addr, "QUIT"))
                break
            if len(msg) == 2:
                if msg[0] == "REPORT":
                    if not check_ipp(msg[1]):
                        q.put((addr, "WRONGIPP"))
                    else:
                        q.put((addr, "REPORT", msg[1]))
                else:
                    q.put((addr, "???"))
            elif len(msg) > 3:
                if msg[1] == "GET" and msg[2] == "LIST":
                    if not check_ipp(msg[0]):
                        q.put((addr, "WRONGIPP"))
                    else:
                        movie_name = l.split(" GET LIST ")[1][1:-1]
                        q.put((addr, "SENDLIST", msg[0], movie_name))
                else:
                    q.put((addr, "???"))
            else:
                q.put((addr, "???"))
    t = Thread(target=handle)
    return t


# Works through the queue.
def consumer(q):
    # This calls the function that initializes the server before starting the infinite loop
    handle_acceptall(q)

    def consume():
        while True:
            e = q.get()
            if e[1] == 'QUIT':
                clients[e[0]].sendall(b('Goodbye!'))
            if e[1] == 'WRONGIPP':
                clients[e[0]].sendall(b('Invalid IP:Port entered.'))
            elif e[1] == 'REPORT':
                clients[e[0]].sendall(b('Your report has been noted.'))
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    report_ipp = e[2].split(":")
                    # Try to connect to reported IPP
                    print("Trying to access", e[2], "...")
                    try:
                        s.connect((report_ipp[0], int(report_ipp[1])))
                        time.sleep(1)
                        s.close()
                    # If it fails, delete all mentions of this configuration from our storage
                    except (TimeoutError, ConnectionRefusedError, OSError):
                        print("Could not connect, deleting IPP...")
                        with open("files.txt", "r") as f:
                            lines = f.readlines()
                            for idx, line in enumerate(lines):
                                split = line[:-1].split(" ")
                                split = [x for x in split if x != e[2]]
                                lines[idx] = " ".join(split)+line[-1]
                        with open("files.txt", "w") as f:
                            f.writelines(lines)
            elif e[1] == 'SENDLIST':
                flag = False
                modify_line = []
                with open("files.txt", "r") as f:
                    for idx, line in enumerate(f):
                        split1 = line[:-1].split(" IPP")
                        if split1[0] == e[3]:
                            flag = True
                            ipp_list = []
                            if len(split1[1]) > 1:
                                split2 = split1[1][1:].split(" ")
                                # Give 5 IPs that are different than the one he is using (for reentered users)
                                split2 = [x for x in split2 if x != e[2]]
                                if len(split2) > 5:
                                    ipp_list = [split2[x] for x in np.random.choice(len(split2), 5, replace=False)]
                                else:
                                    ipp_list = split2
                            clients[e[0]].sendall(b("SOL"))
                            for ipp in ipp_list:
                                clients[e[0]].sendall(b(ipp))
                            clients[e[0]].sendall(b("EOL"))
                            # Add the new IP to the list (if it's not already on)
                            if not e[2] in split1[1].split(" "):
                                modify_line = [idx, line]

                    if not flag:
                        clients[e[0]].sendall(b('No such file found'))
                        time.sleep(.1)
                if modify_line:
                    with open("files.txt", "r") as f:
                        lines = f.readlines()
                        lines[modify_line[0]] = lines[modify_line[0]][:-1]+" "+e[2]+lines[modify_line[0]][-1]
                    with open("files.txt", "w") as f:
                        f.writelines(lines)
                if not flag:
                    clients[e[0]].sendall(b('No such file found'))
                    time.sleep(.1)
            else:
                try:
                    clients[e[0]].sendall(b('Unknown command'))
                except ConnectionAbortedError:
                    print("Connection was closed before sending")
    t = Thread(target=consume)
    return t


# Transforms string for sending using utf8
def b(msg):
    return bytes(msg+"\r\n", "utf8")


# Checks if a string adheres to the IP:Port configuration
def check_ipp(ipp):
    aa = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$", ipp)
    return aa


if __name__ == "__main__":
    main()