#  - Inputs
#     libr-file
#     (chunk_list optional)
# - Outputs
import socket
import time
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
    peer_server(IPP_peer)

    # Start queues for working as a server and as a client in the network
    # As a server, we are taking in requests for chunks or requests to get he list of chunks we have
    # As a client, we are requesting specific chunks or the lists of chunks that other peers have

    # Connect to the tracker to get the IPs of clients associated with stuff we want to share/get
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((tracker_ip, int(tracker_port)))

        msg = IPP_peer + ' GET LIST ' + name_stuff
        s.sendall(bytes(msg+"\r\n", "utf8"))

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

    # Chunk list saves the bytestreams of each chunk using the index of the chunk in the list
    # If we have the file (i.e. we are only here for seeding, we put the file into the chunk list
    try:
        i = 0
        assert(os.path.isfile('./'+libr_file.replace('.libr', '')))
        # The libr file has the same name as the file, only with a .libr at the end
        with open(libr_file.replace('.libr', ''), 'rb') as f:
            # We break down the file
            print("Creating books...")
            while True:
                data = f.read(1024 * booksize)
                # If a chunk is corrupted for some reason, leave it empty in chunk_list, so you can redownload it
                # if str(hashlib.md5(data).hexdigest()) == sha1_list[i]:

                if data == b'':
                    f.close()
                    break

                chunk_list[i] = data
                i += 1

        try:
            assert (os.path.isfile('./' + libr_file.replace('.libr', '.cl')))
            with open(libr_file.replace('.libr', '.cl'), 'rb') as f:
                chunk_list = pickle.load(f)
        except AssertionError:
            with open(libr_file.replace('.libr', '.cl'), 'wb') as f:
                pickle.dump(chunk_list, f)

    # We don't have the file to share, but we may have the chunk list file
    except AssertionError:
        try:
            assert (os.path.isfile('./' + libr_file.replace('.libr', '.cl')))
            with open(libr_file.replace('.libr', '.cl'), 'rb') as f:
                chunk_list = pickle.load(f)
        except AssertionError:
            with open(libr_file.replace('.libr', '.cl'), 'wb') as f:
                pickle.dump(chunk_list, f)

    server_q = peer_client(iplist, tracker_ipp)

    # Main, loop, we want to get all chunks, for this we want to fill until chunk_present is only 1s
    list_loop = 0

    global list_of_chunks_they_have
    list_of_chunks_they_have = np.zeros([len(iplist), len(chunk_list)])
    chunks_we_want = np.array([val == b"" for val in chunk_list])

    while np.sum(chunks_we_want) > 0:
        # Global variable, each peer in the network gives their "chunk_present", this will be added into this np.array

        # We ask each peer for a specific stuff which chunks they have
        # Every 10th loop
        if list_loop == 0 or (any(list(list_of_chunks_they_have.flatten())) and list_loop % 10 == 0):
            for idx, ipp in enumerate(iplist):
                ask_which_chunks(ipp, name_stuff, server_q, idx)

        # Indices of chunks we don't have yet
        chunks_we_want = np.array([val == b"" for val in chunk_list])
        # Sum the matrix over each chunk, so that we see how many peers have a specific chunk
        chunk_commonality = np.sum(list_of_chunks_they_have, axis=0)
        chunk_availability = chunk_commonality
        # Tis is only used so we know which chunks don't appear once
        chunk_availability[chunk_availability != 0] = 1
        # Now we also forget about all the chunks we already have
        # chunk_availability = chunk_availability * np.array(chunks_we_want)
        chunk_commonality = chunk_commonality * chunk_availability * chunks_we_want
        chunk_commonality[chunk_commonality == 0] = np.inf
        # Sort the chunks so we look at them in order or rarity
        chunks_we_can_get_sorted = np.argsort(chunk_commonality)
        chunks_we_can_get_sorted = chunks_we_can_get_sorted[:int(sum(chunk_availability))]
        # Give requests for all the peers, choose peer randomly among each who has a specific chunk we need
        requests_send = np.zeros([len(list_of_chunks_they_have), 1])
        print("No remaining chunks:", np.sum(chunks_we_want))

        for chunk in chunks_we_can_get_sorted:
            listylist = list_of_chunks_they_have[:, chunk]
            # Peers who have the chunk
            listylistidxs = [idx for idx, val in enumerate(listylist) if val == 1]
            # Peers who have the chunk and are available
            available_peers = [idx for idx, val in enumerate(requests_send) if val <= 1]
            candidates = [candidate for candidate in available_peers if candidate in listylistidxs]

            if candidates:
                candidate = rd.choice(candidates)
                requests_send[candidate] += 1
                chunk_list[chunk] = ask_for_chunk(iplist[candidate], chunk, server_q, candidate)
        time.sleep(3)
        list_loop += 1
    # Write the chunks into the file when we have all of them
    with open(libr_file.replace('.libr', ''), 'wb') as f:
        for chunk in chunk_list:
            f.write(chunk)
    try:
        while True:
            continue
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
def ask_which_chunks(server_ipp, stuff, server_q, server_idx):
    server_q.put((server_ipp, 'WHICHCHUNKS', stuff, server_idx))


# Give a request to get a specific chunk from another peer
def ask_for_chunk(server_ipp, chunk, server_q, server_idx):
    server_q.put((server_ipp, 'GETCHUNK', chunk, server_idx))
    return 1


# Transforms string for sending using utf8
def b(msg):
    return bytes(msg+"\r\n", "utf8")


# Starts the queues and threads and server requests
def peer_server(ipp):

    client_q = queue.Queue()
    consumer_clients(client_q, ipp)
    return client_q


def peer_client(iplist, tracker_ipp):

    server_q = queue.Queue()
    consumer_servers(server_q, iplist, tracker_ipp).start()
    return server_q


# This is the client, opens the socket in order to receive requests
def handle_servers(server_q, iplist, tracker_ipp):

    def cocosete(ipp):
        # create a socket that listens (on a port of your choice)
        ipp_head = ipp.split(":")

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ipp_head[0], int(ipp_head[1])))
            servers[ipp] = s
        except (TimeoutError, ConnectionRefusedError, OSError):
            # Connect to the tracker to get the IPs of clients associated with stuff we want to share/get
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((tracker_ipp[0], int(tracker_ipp[1])))

                msg = 'REPORT ' + ipp
                s.sendall(b(msg))
                # Get the list of IPs
                ans = rl(s)
                if ans == 'Your report has been noted.':
                    s.close()
                else:
                    print("Protocol violation")
                    s.close()
        while True:
            pass

    for ipp in iplist:
        Thread(target=cocosete, args=([ipp])).start()
    return 1


# This is the server, opens the socket in order to receive requests
def handle_clients(client_q, ipp):

    def handle():
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
            clients[addr] = socket_c
            print('Got connection from', addr)
            # The producer will handle connections with clients
            producer(socket_c, addr, client_q).start()

    Thread(target=handle).start()
    return 1


# Takes care of incoming messages from the client, puts them in a queue
def producer(socket, addr, client_q):

    # Check for timeout if peer doesn't say anything
    def handle():
        while True:
            # read two lines then ignore anything from this client...
            try:
                l = rl(socket)
            except ConnectionResetError:
                print("Connection to a peer was forcibly closed.")
                break
            print("RECEIVED Message:", l)
            commandlist = l.split(" ")
            if len(commandlist) == 3:
                if commandlist[0] == "Copy" and commandlist[1] == "book":
                    book_id = commandlist[2]
                    client_q.put((addr, "GETCHUNK", book_id))
            elif commandlist[0] == "Books" and commandlist[-1] == "?":
                stuff_name = l.split('"')[1]
                client_q.put((addr, "WHICHCHUNKS", stuff_name))
            else:
                client_q.put((addr, "???", ""))
    t = Thread(target=handle)
    return t


# Client side perspective
def consumer_servers(server_q, iplist, tracker_ipp):

    # This calls the function that initializes the server before starting the infinite loop
    handle_servers(server_q, iplist, tracker_ipp)

    def consume():
        while True:
            e = server_q.get()
            server_ipp = e[0]
            s = servers[server_ipp]
            command = e[1]
            book_idx = e[2]
            server_idx = e[3]

            if command == "WHICHCHUNKS":
                s.sendall(b("Books " + book_idx + " ?"))
                ans = rl(s)
                if ans == "SOL":
                    chunk_list_from_server = []
                    ans = rl(s)
                    while ans != "EOL":
                        chunk_list_from_server.append(int(ans))
                        ans = rl(s)
                global list_of_chunks_they_have
                chunk_mask = [idx in chunk_list_from_server for idx in range(list_of_chunks_they_have.shape[1])]
                list_of_chunks_they_have[server_idx, :] = np.array(chunk_mask)

            if command == "GETCHUNK":
                global chunk_list
                s.sendall(b("Copy book " + str(book_idx)))

                ans = rl(s)
                if ans == "Commencing bytestream":
                    bs = s.recv(1024*8)
                else:
                    print("Protocol violation, 'commencing bytestream'")
                chunk_list[book_idx] = bs
                print(chunk_list[1])

            elif command == "???":
                s.sendall(b("Unknown command"))

    t = Thread(target=consume)
    return t


# Server side perspective.
def consumer_clients(client_q, ipp):
    # This calls the function that initializes the server before starting the infinite loop
    handle_clients(client_q, ipp)

    def consume():
        while True:
            e = client_q.get()
            client_idx = e[0]
            command = e[1]
            book = e[2]

            global chunk_list

            if command == "WHICHCHUNKS":
                try:
                    clients[client_idx].sendall(b("SOL"))

                    chunk_present = [x != b'' for x in chunk_list]
                    for idx in [idx for idx,val in enumerate(chunk_present) if val == 1]:
                        clients[client_idx].sendall(b(str(idx)))


                    clients[client_idx].sendall(b("EOL"))

                except ConnectionResetError:
                    print("Client force closed connection")

            if command == "GETCHUNK":
                clients[client_idx].sendall(b("Commencing bytestream"))

                clients[client_idx].sendall(chunk_list[int(book)])

    Thread(target=consume).start()
    return 1


# Creates a file which associates the name of the stuff with their respective (libr-) filename
def lib_bijection(stuffname, filename):
    bij_dict = {}
    with open('filenames.bi', 'wb') as output:
        bij_dict[stuffname[1:-1]] = filename
        pickle.dump(bij_dict, output)


main('HALAL.jpg.libr')