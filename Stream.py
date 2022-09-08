#!/usr/bin/python3
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# This can also be accomplished by using s = socket.socket(), because AF_INET, and SOCK_STREAM are defaults

ipaddr = '127.0.0.1'
port = 54321

s.connect((ipaddr, port))

#To send a string as a bytes-like object, add the prefix b to the string. \n is used to go to the next line
s.send(b'Hello')

# It is recommended thet the buffersize used with recvfrom is a power of 2 and not a very large number of bits
response, conn = s.recvfrom(1024)

# In order to recieve a message that is sent as bytes-like-object, you must decode into utf-8 (default)
print(response.decode())

s.close()
