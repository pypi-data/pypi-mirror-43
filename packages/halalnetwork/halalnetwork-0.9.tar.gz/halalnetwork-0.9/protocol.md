# 2019-net-b

## Introduction

<dl>
  <dd>
  This is the description of the protocol developed to manage the connections between players and/or with the hub to download/upload stuff in a peer to peer program like BitTorrent.
  </dd>
</dl>

## Process step by step:

<dl>
  <dd>
    This is the process step by step with the protocol, how a player can download or upload stuff with our application.
  </dd>
  <dt>
    1. Player tries to connect with the hub
  </dt>
  <dd>
    a.  One player P1 start TCP-IP-connection with the hub. It knows the IP:Port address of the hub thanks to the application.
  </dd>
  <dd>
    b.  P1 send a message to the hub. 
  </dd>
  
```  
Format:
  IP:Port GET LIST “the_stuff_we_need”
 
Example:
  161.3.1.28:8652 GET LIST “Movie Lord of The Ring II”
```

<dt> 
  2. Response of the hub 
</dt>
  <dd>
    a.  If the hub has less than X connections, it accepts the connection. (X depends on the capacity of the machine)
  </dd>
  <dd>
    b.  Else it adds the player to a waiting queue of players (FiFO list)
  </dd>
  <dd>
    c.  When one player closes the connection with the hub, the hub accepts the connection, if the timeout of the TCP-protocol doesn’t close the connection or start the connection with the first player of the queue.
  </dd>
<dt>
    3. When the connection between player and hub is established:
</dt>
  <dd>
    a.  Hub responds with messages as strings containing the list of at most 5 randomly selected players having the stuff we need.
        *SOL* symbolizes START OF LIST and EOL symbolizes END OF LIST.
  </dd>
  
```
Format:
  SOL
  IP:Port
  IP:Port
  ...
  EOL
 
Example:
  SOL
  161.3.1.28:8652
  52.20.2.7:7456
  EOL
```

<dt>
  4. When player has the list of players:
</dt>
  <dd>
    a. Player sends message to the hub to close the connection
  </dd>
  
```
Format:
  “List received, Close connection”
 
Example:
  List received, Close connection
```

  <dd>
    b.  Hub closes connection with the player who initiated the connection.
  </dd>
  <dd>
    c.  Player tries to connect to each player of the IP:Port in the list with the message:
  </dd> 

```
Format:
  "Books “the_stuff_we_need” ?"
 
Example:
  Books “Movie Lord of The Ring II” ?
```

<dt>
 5. When a player receives a request to know which books it has:
</dt>
  <dd>
    a.  The other player responds with the message:
  </dd>  
 
```
Format:
  “
  SOL
  Books:
  ID-X
  ID-Y
  …
  EOL”
  
 
Example:
  SOL
  Books:
  125242472
  487368678
  EOL
```

  <dd>
    b.  The ID of a book is determined by the relative position of the of its corresponding SHA1 in the library file (1st SHA1 is "0", 2nd SHA1 is "1", etc).
  </dd>

<dt>
6. When we collected the information about all books:
</dt>
  <dd>
    a.  We select the books with lowest occurrence.
  </dd>
  <dd>
    b.  We connect to players that have those books and start to download with this message:
  </dd>  
  
```
Format:
  “Copy book ID-X”
 
Example:
  Copy book 125242472
```

  <dd>
    c.  In a case there are books that multiple people have, we get the books from the guy that responded to us first.
  </dd>
  <dd>
    d.  When the book is received -> check the checksum
  </dd>
  <dd>
    -> if the checksum is ok, continue with connection.
  </dd>
  <dd>
    -> if the checksum is wrong, try to download from the same player again. if this time after the download the checksum will be wrong again -> go to step 4.c.
  </dd>

<dt> 
  7.  Close the connection:
</dt>

  <dd>
    a.  if we decided to leave only
  </dd>

<dt>
  8.  Sending a file as bytestream:
</dt>

  <dd>
    a.  The Sender sends a message: 
  </dd>
  
```
Format:
  "Commencing bytestream"
  
Example:
  Commencing bytestream
```

  <dd>
    b.  The Receiver starts listening for the bytetream. The symbol "¶" in ASCII code in bytes (10110110) symbolizes the start and end of the transmission.
  </dd>
  
```
Format:
  "10110110
   BYTE-1
   BYTE-2
   ...
   10110110
   "

Example:
  10110110
  01101110
  10010010
  10110110
```
  
</dl>                             
  

## Sample library file

```
# the address of the hub
hub : 92.168.6.66:42000
# the name of the stuff
stuff_name : Synopsis Movie Lord of The Ring II
# the size of the stuff
stuff_size : 5Ko
# the size used for books
books_size : 2Ko
# SHA1 of each books
books listed :
cf23df2207d99a74fbe169e3eba035e633b65d94
cf23df22085535035e633bfbdfb035e633b65d94
cf23df2207d99a74fbe169e3ebadh583585635j5
```
