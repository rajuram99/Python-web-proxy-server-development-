
from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# bind to the port
tcpSerSock.bind(('localhost',8888))
# start listening
tcpSerSock.listen(10) # become a server socket


while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = repr(tcpCliSock.recv(10000))
    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check whether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n"))
        tcpCliSock.send(bytes("Content-Type:text/html\r\n"))
        tcpCliSock.send(bytes("Cache hit found hence message generated!!"))
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxy server
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.","",1)
            print(hostn)
            try:
                # Connect to the socket to port 80
                c.bind((addr,80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")
                # Read the response into buffer
                buffer = c.recv(1024)
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                c.send(buffer)
                tmpFile.write(buffer)
            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            tcpCliSock.send(bytes("HTTP/1.1 404 ERROR\n"+"Content-Type: text/html\n"+"\n"+"<html><body>File Not "
                                                                                          "found</body></html>\n"))
    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()

