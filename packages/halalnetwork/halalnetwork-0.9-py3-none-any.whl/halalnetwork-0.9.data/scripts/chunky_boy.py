import hashlib
import socket
import os

booksize = 8
Lfill = []
Lcode = []

# Function that generates the LIB file
def libgenerator(tracker_address, libfilename, filename, userfilename, filesize, lib_booksize):

    with open(libfilename,'w') as output:

        output.write('# the address of the tracker\n')
        output.write('hub : '+tracker_address+'\n')
        output.write('# the name of the stuff\n')
        output.write('stuff_name : '+userfilename+'\n')
        output.write('# the size of the stuff\n')
        output.write('stuff_size : '+ filesize +'Ko\n')
        output.write('# the size used for books\n')
        output.write('books_size : ' + lib_booksize +'Ko\n')
        output.write('# SHA1 of each books \nbooks listed : \n')
        with open(filename, "rb") as input:
            while True:
                data = input.read(1024 * int(lib_booksize))
                if data == b"":
                    input.close()
                    break
                output.write(str(hashlib.md5(data).hexdigest())+'\n')

# Associates the name of stuff with the filename so that we can locate the requested files
# (Assocoiate the name of the stuff with the accordingly generated lib file
def lib_biyection(stuffname, filename):

    with open('filenames.bi', 'w') as output:
        for i in range(len(filename)):
            output.write(stuffname[i]+' : '+ filename[i] +'\n')


# Available port finder
def openportfinder(inPort=5000, endPort=7000):

    def tryport(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = False
        try:
            sock.bind(("0.0.0.0", port))
            result = True
        except:
            pass

        sock.close()
        return result

    for i in range(inPort, endPort):
        if tryport(i):
            return i

# Stuff name finder
def stuffname(libfile):
    with open(libfile) as input:
        content = input.readlines()
        stuffName = content[3].strip().split('name : ')[1]
        print(stuffName)

stuffnames = ['Lord of Yarrak', 'El Cacique Guaicaipuro','Er Conde der Guacharo']
filenames = ['input.jpg','music.mp3','archive.zip']

lib_biyection(stuffnames, filenames)

for i in range(len(filenames)):
    libgenerator(str(socket.gethostbyname(socket.gethostname()) )+':1234', 'generated_from_input_'+str(filenames[i])+'.lib',
             str(filenames[i]), str(stuffnames[i]), str((os.stat(filenames[i])).st_size), str(booksize))
