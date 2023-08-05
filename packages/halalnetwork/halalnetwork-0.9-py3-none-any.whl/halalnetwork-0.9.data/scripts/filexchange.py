# with open("input.jpg", "rb") as input:
#     with open("output.jpg", "wb") as output:
#         while True:
#             data = input.read(1024*8)
#             if data == b"":
#                 break
#             output.write(data)
#             print(data)

from threading import Thread
import hashlib
import socket
import random
import queue
import time
import os

booksize = 8 #Ko

# Main function
def main(): # called at the end of the file

    # Prepares the queue of tasks to be performed by the consumer
    q = queue.Queue()

    # Initiate the consumer program who deals with printings
    c = consumer(q)
    c.daemon = True # NB: the program terminates when all non-daemon thread are done
    c.start()

    # Start to receive request from clients
    server(q).start()
    time.sleep(0.5)
    client()


# This is the server, opens the socket in order to receive requests
def server(q):
    def handle():
        # create a socket that listens (on a port of your choice)

        server_socket = socket.socket()
        port = 4565
        server_socket.bind(('192.168.43.29', port))
        print("socket binded to %s" % port)
        server_socket.listen()
        print("socket is listening")
        # accept new clients connections,
        # and start a handle_client thread every time


        # a forever loop until we interrupt it or
        # an error occurs
        while True:
            # Establish connection with client.
            socket_c, addr = server_socket.accept()
            print ('Got connection from', addr)
            # The producer will handle connections with clients
            producer(socket_c,q).start()

    t = Thread(target=handle)
    return t


# handle_client returns a Thread that can be started, i.e., use: handle_client(.......).start()
def producer(socket,q):
    def handle():

        # WE TELL CONSUMER THAT I HAVE NEW CONNECTION AND DISPLAY IT

        # loop over the received data, ignoring (or just printing) this data for now (e.g., use netutils to read lines)
        # be sure to end the loop when the connection is closed (readLine returns None or throws an exception)

        while True:
            # read two lines then ignore anything from this client...

            # $$$ PUT STUFF ON QUEUE IF I HAVE THE MAGIC WORD
            l = socket.recv(1024*booksize)
            print("RECEIVED Message:", l)
            # print("SHA1:", make_sha1(l))

            q.put(l)

            if l == b"":
                break
            # ... ignore the rest

        output = open("output.jpg", "wb")
        print('ready to get stuff')
        while True:

            bstr = q.get()
            if bstr == b"":
                # print(bstr)
                output.close()
                break
            output.write(bstr)

        with open("output.jpg", "rb") as output_to_check:
            # read contents of the file
            data_output = output_to_check.read()
            # pipe contents of the file through
            md5_returned_output = hashlib.md5(data_output).hexdigest()
            print("output.jpg code: ", md5_returned_output)
        try:
            os.rename("output.jpg", "{0}.jpg".format(md5_returned_output))
        except:
            pass

        # Later, we will use move_value_right(i, by) and increase the i variable by
            # DONE

    t = Thread(target=handle)
    return t


def consumer(q):

    # This calls the function that initializes the server before starting the infinite loop
    server(q)

    print('doing something 1')

    def consume():

        pass
        # with open("output.jpg","rb") as output_to_check:
        #     print('doing something 2')
        #
        #     # read contents of the file
        #     data_input = output_to_check.read()
        #     # pipe contents of the file through
        #     md5_returned_input = hashlib.md5(data_input).hexdigest()
        #     print("input.jpg  code: ", md5_returned_input)
        #     # output_to_check.close()

        # with open("input.jpg", "rb") as input_to_check:
        #     # read contents of the file
        #     data_input = input_to_check.read()
        #     # pipe contents of the file through
        #     md5_returned_input = hashlib.md5(data_input).hexdigest()
        #     print("input.jpg  code: ", md5_returned_input)

    t = Thread(target=consume)
    return t


def client(): # called at the end of the file
    # pass # TODO, taking inspiration of the rest

    TCP_IP = '192.168.43.32'
    TCP_PORT = 3131
    # BUFFER_SIZE = 20

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TCP_IP, TCP_PORT))

        with open("input.jpg", "rb") as input:
            while True:
                data = input.read(1024 * booksize)
                if data == b"":
                    s.sendall(data)
                    input.close()
                    break
                s.sendall(data)
                # print(data)

        s.close()


if __name__== "__main__":
  main()
