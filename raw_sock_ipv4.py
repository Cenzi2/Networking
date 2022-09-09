#!/usr/bin/env python3

#for building the socket
import socket

#for system level commands
import sys

#for  establishing the packet structure. This will allow direct access to the methods and functions in the struct module
from struct import *

# Create a raw socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
except socket.error as msg:
    print(msg)
    sys.exit()

packet = ''
src_ip = "10.1.0.2"
dst_ip = "10.3.0.2"

#add the ipv4 header information
ip_ver_ihl = 69     #this is putting the decimal conversion of 0x45 for version and Internet Header Length
ip_tos = 0      # This combines the DSCP and ECN fields
ip_len = 0      # The Kernel will fill in the actual length of the packet
ip_id = 12345   # This sets up the ip identification for the packet
ip_frag = 0     # This sets the fragmentation to off
ip_ttl = 64     # This determines the TTL of the packet when leaving the machine
ip_proto = 16   # This sets up the IP protocol to 16 (CHAOS). If this was 6 (TCP) or 17 (UDP) additional headers would be required
ip_check = 0    # The kernel will fill in the checksum for the packet
ip_srcadd = socket.inet_aton(src_ip) # inet_aton(string) will convert an ip address to a 32 bit binary number
ip_dstadd = socket.inet_aton(dst_ip) # inet_aton(string) will convert an ip address to a 32 bit binary number

ip_header = pack('!BBHHHBBH4s4s', ip_ver_ihl, ip_tos, ip_len, ip_id, ip_frag, ip_ttl, ip_proto, ip_check, ip_srcadd, ip_dstadd)    # B=byte, H=halfword (2bytes), 4s=4Byte string object , used to dentoe the size of each of the followiong variables in big endian format

message = b'This is a message'
packet = ip_header + message

# send the packet
s.sendto(packet, (dst_ip, 0))
