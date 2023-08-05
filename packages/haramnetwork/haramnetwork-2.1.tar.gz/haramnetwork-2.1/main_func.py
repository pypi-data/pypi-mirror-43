#  - Inputs
#     libr-file
#     (chunk_list optional)
# - Outputs
import socket
import time

import netutils
from netutils import read_line as rl
import numpy as np
import random as rd
import queue
from threading import Thread
import os
import dill as pickle

clients = {}
servers = {}


def main(libr_file):

    global chunk_list

    # Open the libr file, get info to connect to tracker, SHA1, name, ...
    with open(libr_file) as input:
        content = input.readlines()

        # Retrieve name of stuff from lib
        name_stuff = '"' + content[3].strip().split('name : ')[1] + '"'

        # We create a file which associates the name of the libr file with the name of the stuff
        # This will help us later finding the right chunks associated with a name
        lib_bijection(name_stuff, libr_file)

        # Retrieve IP of the HUB
        tracker_ip, tracker_port = content[1].strip().split('hub : ')[1].split(":")
        tracker_ipp = [tracker_ip, tracker_port]

        # Retrieve Booksize
        booksize = int(content[7].strip().split('size : ')[1].replace('Ko', ''))

        # Create empty list for chunks from libr file and get list of SHA1
        sha1_list = content[10:]
        chunk_list = [b"" for x in content[10:]]

    # Combining the ipv4 and the available port to connect to tracker
    IPP_peer = socket.gethostbyname(socket.gethostname()) + ":" + str(openportfinder(5500))
    client_q = peer_server(IPP_peer)

    # Start queues for working as a server and as a client in the network
    # As a server, we are taking in requests for chunks or requests to get he list of chunks we have
    # As a client, we are requesting specific chunks or the lists of chunks that other peers have

    print(1)

    # Connect to the tracker to get the IPs of clients associated with stuff we want to share/get
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((tracker_ip, int(tracker_port)))

        msg = IPP_peer + ' GET LIST ' + name_stuff
        s.sendall(bytes(msg+"\r\n", "utf8"))
        time.sleep(.1)
        # Get the list of IPs
        ans = rl(s)
        if ans == "SOL":
            iplist = []
            while True:
                ans = rl(s)
                if ans == "EOL":
                    break
                iplist.append(ans)
        s.sendall(b("List received, Close connection"))
        ans = rl(s)
        if ans == "Goodbye!":
            s.close()

    print(2)
    # Chunk list saves the bytestreams of each chunk using the index of the chunk in the list
    # If we have the file (i.e. we are only here for seeding, we put the file into the chunk list
    try:
        i = 0
        assert(os.path.isfile('./'+libr_file.replace('.libr', '')))
        # The libr file has the same name as the file, only with a .libr at the end
        with open(libr_file.replace('.libr', ''), 'rb') as f:
            # print(f)
            # We break down the file
            print("Creating books...")
            while True:
                data = f.read(1024 * booksize)
                # print('making chunklist')
                # print('data sha1 is:',hashlib.md5(data).hexdigest())
                # If a chunk is corrupted for some reason, leave it empty in chunk_list, so you can redownload it
                # if str(hashlib.md5(data).hexdigest()) == sha1_list[i]:

                if data == b'':
                    f.close()
                    break

                chunk_list[i] = data
                i += 1

        # print('resulting list')
        # print(chunk_list)
        try:
            assert (os.path.isfile('./' + libr_file.replace('.libr', '.cl')))
            with open(libr_file.replace('.libr', '.cl'), 'rb') as f:
                chunk_list = pickle.load(f)
        except AssertionError:
            # print("now we create shit")
            # print(chunk_list)
            with open(libr_file.replace('.libr', '.cl'), 'wb') as f:
                pickle.dump(chunk_list, f)

    # We don't have the file to share, but we may have the chunk list file
    except AssertionError:
        # print(5)
        try:
            assert (os.path.isfile('./' + libr_file.replace('.libr', '.cl')))
            with open(libr_file.replace('.libr', '.cl'), 'rb') as f:
                chunk_list = pickle.load(f)
        except AssertionError:
            print("now we create shit")
            with open(libr_file.replace('.libr', '.cl'), 'wb') as f:
                pickle.dump(chunk_list, f)

    print(3)
    server_q = peer_client(iplist, tracker_ipp)

    # We determine the chunks that we need, this is a mask of [1,0,0,1,0,0,1,...] which has 1 for each chunk we have
    # print(chunk_list[0])
    chunk_present = [x != b'' for x in chunk_list]
    print('the chunks are present')
    # print(chunk_present)
    # Main, loop, we want to get all chunks, for this we want to fill until chunk_present is only 1s
    print(4)
    while not all(chunk_present):
        print(5)
        # Global variable, each peer in the network gives their "chunk_present", this will be added into this np.array
        global list_of_chunks_they_have
        list_of_chunks_they_have = np.zeros([len(iplist), len(sha1_list)])
        # We ask each peer for a specific stuff which chunks they have
        for idx, ipp in enumerate(iplist):
            ask_which_chunks(idx, name_stuff, server_q)

        # Wait some time for everybody to give the list, ideally we would use multiprocessing and join here though...
        time.sleep(3)

        # Indices of chunks we don't have yet
        chunks_we_want = [i for i, val in enumerate(chunk_list) if val == b""]
        # Sum the matrix over each chunk, so that we see how many peers have a specific chunk
        chunk_commonality = np.sum(list_of_chunks_they_have, axis=0)
        chunk_availability = chunk_commonality
        # Tis is only used so we know which chunks don't appear once
        chunk_availability[chunk_availability != 0] = 1
        # Now we also forget about all the chunks we already have
        # print(chunk_availability.shape)
        chunk_availability = chunk_availability * chunks_we_want
        chunk_commonality = chunk_commonality * chunk_availability
        chunk_commonality[chunk_commonality == 0] = np.inf
        print(7)
        # Sort the chunks so we look at them in order or rarity
        chunks_we_can_get_sorted = np.argsort(chunk_commonality)
        chunks_we_can_get_sorted = chunks_we_can_get_sorted[:int(sum(chunk_availability))]
        # Give requests for all the peers, choose peer randomly among each who has a specific chunk we need
        available_peers = range(len(iplist))
        for chunk in chunks_we_can_get_sorted:
            listylist = list_of_chunks_they_have[:, chunk]
            # Peers who have the chunk
            listylistidxs = [x for x, val in listylist if val == 1]
            # Peers who have the chunk and are available
            candidates = [x for x in available_peers if x in listylistidxs]
            if candidates:
                candidate = rd.choice(candidates)
                del available_peers[candidate]
                chunk_list[chunk] = ask_for_chunk(candidate, chunk, server_q)
        time.sleep(5)
    # Write the chunks into the file when we have all of them
    with open(libr_file.replace('.libr', ''), 'wb') as f:
        for chunk in chunk_list:
            f.write(chunk)
    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        print("Leaving network, goodbye!")


# Available port finder
def openportfinder(inPort=5000, endPort=7000):

    def tryport(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = False
        try:
            sock.bind(("0.0.0.0", port))
            result = True
        except socket.error:
            pass

        sock.close()
        return result

    for i in range(inPort, endPort):
        if tryport(i):
            return i


# Give a request to get the chunk_present of another peer
def ask_which_chunks(server_idx, stuff, q):
    print("Server_idx:", server_idx)
    q.put((server_idx, 'WHICHCHUNKS', stuff))


# Give a request to get a specific chunk from another peer
def ask_for_chunk(server_idx, chunk, q):
    q.put((server_idx, 'GETCHUNK',chunk))
    return 1


# Transforms string for sending using utf8
def b(msg):
    return bytes(msg+"\r\n", "utf8")


# Starts the queues and threads and server requests
def peer_server(ipp):

    client_q = queue.Queue()
    c = consumer_clients(client_q, ipp)
    c.daemon = True
    c.start()
    return client_q


def peer_client(iplist, tracker_ipp):

    server_q = queue.Queue()
    c2 = consumer_servers(server_q, iplist, tracker_ipp)
    return server_q


# This is the client, opens the socket in order to receive requests
def handle_servers(q, iplist, tracker_ipp):
    print('habdle2 ipps: ', iplist)

    def cocosete(ipp):
        print('handle2 handle!!<<<<<<<<<<<<<<<<<<<<<<<')
        print(ipp)
        # create a socket that listens (on a port of your choice)
        ipp_head = ipp.split(":")
        print('PIPI:', ipp_head)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ipp_head[0], int(ipp_head[1])))
            print("hello?")
            servers[ipp] = s
        except (TimeoutError, ConnectionRefusedError, OSError):
            # Connect to the tracker to get the IPs of clients associated with stuff we want to share/get
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((tracker_ipp[0], int(tracker_ipp[1])))

                msg = 'REPORT ' + ipp
                s.sendall(b(msg))
                time.sleep(.1)
                # Get the list of IPs
                ans = rl(s)
                if ans == 'Your report has been noted.':
                    s.close()
                else:
                    print("Protocol RAPE")
                    s.close()
        while True:
            pass

    print('HANDLE 2 GOING TO ENTER HANDLE')
    for ipp in iplist:
        print("Ipp: ", ipp)
        t = Thread(target=cocosete, args=([ipp]))
        t.daemon = True
        t.start()
    return 1


# This is the server, opens the socket in order to receive requests
def handle_clients(q, ipp):

    def handle():
        print("helloooo")
        # create a socket that listens (on a port of your choice)
        iplist = ipp.split(":")

        server_socket = socket.socket()
        port = iplist[1]  # np.random.randint(1000,9999)
        server_socket.bind(('', int(port)))
        print("socket bound to %s" % port)
        server_socket.listen()
        print("socket is listening")
        print("Server IP address: ", iplist[0])

        while True:
            # Establish connection with client.
            socket_c, addr = server_socket.accept()
            print(addr)
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
            print("RECEIVED Message:", l)
            commandlist = l.split(" ")
            if len(commandlist) == 3:
                if commandlist[0] == "Copy" and commandlist[1] == "book":
                    book_id = commandlist[2]
                    q.put((addr, book_id))
            else:
                q.put((addr, "???"))
    t = Thread(target=handle)
    return t


# Client side perspective
def consumer_servers(q, iplist, tracker_ipp):

    print('the iplist: ', iplist)
    # This calls the function that initializes the server before starting the infinite loop
    handle_servers(q, iplist, tracker_ipp)

    print('waait a second nigga :O')
    time.sleep(3)

    def consume():
        while True:
            e = q.get()
            if len(e)==0: continue
            server_idx = e[0]
            print(servers)
            print('serv idx', server_idx)
            s = servers[server_idx]
            command = e[1]
            book_idx = e[2]

            if command == "WHICHCHUNKS":
                s.sendall("Books " + book_idx + " ?")
                ans = rl(s)
                global list_of_chunks_they_have
                list_of_chunks_they_have[server_idx, :] = ans

            if command == "GETCHUNK":
                global chunk_list
                s.sendall(b("Copy book " + str(book_idx)))

                time.sleep(.1)
                ans = rl(s)
                if ans == "Commencing bytestream":
                    bs = rl(s)
                else:
                    print("Protocol violation, 'commencing bytestream'")
                chunk_list[book_idx] = bs

    t = Thread(target=consume)
    return t


# Server side perspective.
def consumer_clients(q, ipp):
    # This calls the function that initializes the server before starting the infinite loop
    handle_clients(q, ipp)

    def consume():
        while True:
            e = q.get()
            client_idx = e[0]
            command = e[1]
            stuff = e[2]

            with open('filenames.bi', 'rb') as input:
                filenames = pickle.load(input)
                libr_file = filenames[stuff]
            with open(libr_file.replace('.libr', '.cl'), 'rb') as f:
                chunk_list = pickle.load(f)

            if command == "WHICHCHUNKS":
                clients[client_idx].sendall(b("SOL"))
                time.sleep(.1)
                chunk_present = [x != b'' for x in chunk_list]
                for idx in [idx for idx,val in enumerate(chunk_present) if val == 1]:
                    clients[client_idx].sendall(b(str(idx)))
                    time.sleep(.01)
                clients[client_idx].sendall(b("EOL"))
                time.sleep(.1)

            if command == "GETCHUNK":
                book = e[3]
                clients[client_idx].sendall(b("Commencing bytestream"))
                time.sleep(.1)
                clients[client_idx].sendall(chunk_list[book])

    t = Thread(target=consume)
    print("AWHASFPJA")
    return t


# Creates a file which associates the name of the stuff with their respective (libr-) filename
def lib_bijection(stuffname, filename):
    bij_dict = {}
    with open('filenames.bi', 'wb') as output:
        bij_dict[stuffname] = filename
        pickle.dump(bij_dict, output)


main('07 - Sleeping in Traffic.mp3.libr')