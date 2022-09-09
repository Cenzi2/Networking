  1 #!/usr/bin/env python3
  2 
  3 #for building the socket
  4 import socket
  5 
  6 #for system level commands
  7 import sys
  8 
  9 #for doing an array in the TCP checksum
 10 import array
 11 
 12 #for  establishing the packet structure. This will allow direct access to the methods and functions in the struct module
 13 from struct import *
 14 
 15 # Create a raw socket
 16 try:
 17     s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
 18 except socket.error as msg:
 19     print(msg)
 20     sys.exit()
 21 
 22 packet = ''
 23 src_ip = "10.1.0.2"
 24 dst_ip = "10.3.0.2"
 25 
 26 #add the ipv4 header information
 27 ip_ver_ihl = 69     #this is putting the decimal conversion of 0x45 for version and Internet Header Length
 28 ip_tos = 0      # This combines the DSCP and ECN fields
 29 ip_len = 0      # The Kernel will fill in the actual length of the packet
 30 ip_id = 12345   # This sets up the ip identification for the packet
 31 ip_frag = 0     # This sets the fragmentation to off
 32 ip_ttl = 64     # This determines the TTL of the packet when leaving the machine
 33 ip_proto = 6   # This sets up the IP protocol to 16 (CHAOS). If this was 6 (TCP) or 17 (UDP) additional headers would be required
 34 ip_check = 0    # The kernel will fill in the checksum for the packet
 35 ip_srcadd = socket.inet_aton(src_ip) # inet_aton(string) will convert an ip address to a 32 bit binary number
 36 ip_dstadd = socket.inet_aton(dst_ip) # inet_aton(string) will convert an ip address to a 32 bit binary number
 37 
 38 ip_header = pack('!BBHHHBBH4s4s', ip_ver_ihl, ip_tos, ip_len, ip_id, ip_frag, ip_ttl, ip_proto, ip_check, ip_srcadd, ip_dstadd)    # B=byte, H=halfword (2bytes), 4s=4Byte string object , used to dentoe the size of each of the followiong variables in big endian format
 39 
 40 
 41 # TCP Header Fields
 42 tcp_src = 54321     # source port
 43 tcp_dst = 7777      # destination port
 44 tcp_seq = 454       # sequence number
 45 tcp_ack_seq = 0     # tcp ack sequence number
 46 tcp_data_off = 5    # data offset specifying the size of the tcp header * 4 which is 20
 47 tcp_reserve = 0     # the 3 reserve bits + ns flag in the reserve field
 48 tcp_flags = 0       # tcp flags field before the bits are turned on
 49 tcp_win = 65535     # maximum allowed window size reordered to network order 
 50 tcp_chk = 0         # tcp checksum will be calculated later on
 51 tcp_urg_ptr = 0     # urgent pointer only if urg flag is set
 52 
 53 # combine the left shifted 4 bit tcp offset and the reserve field
 54 tcp_off_res = (tcp_data_off << 4) + tcp_reserve
 55 
 56 
 57 # TCP flags by bit starting from right to left
 58 tcp_fin = 0         # Finished
 59 tcp_syn = 1         # Synchronize
 60 tcp_rst = 0         # Reset
 61 tcp_psh = 0         # Push
 62 tcp_ack = 0         # Acknowledgment
 63 tcp_urg = 0         # Urgent
 64 tcp_ece = 0         # Explicit
 65 tcp_cwr = 0         # Congestion Window Reduced
 66 
 67 # combine the tcp flags by left shifting the bit locations and adding the bits together
 68 tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5) + (tcp_ece << 6) + (tcp_cwr << 7)
 69 
 70 # The ! in the pack format string means big endian network order
 71 tcp_hdr = pack('!HHLLBBHHH', tcp_src, tcp_dst, tcp_seq, tcp_ack_seq, tcp_off_res, tcp_flags, tcp_win, tcp_chk, tcp_urg_ptr)
 72 
 73 user_data = b'Hello! Is this hidden?'
 74 
 75 # Pseudo Header Fields
 76 src_address = socket.inet_aton(src_ip)
 77 dst_address = socket.inet_aton(dst_ip)
 78 reserved = 0
 79 protocol = socket.IPPROTO_TCP
 80 tcp_length = len(tcp_hdr) + len(user_data)
 81 
 82 # pack the pseudo header and combine with user data
 83 ps_hdr = pack('!4s4sBBH', src_address, dst_address, reserved, protocol, tcp_length)
 84 ps_hdr = ps_hdr + tcp_hdr + user_data
 85 
 86 def checksum(data):
 87         if len(data) % 2 !=0:
 88             data +=b'\0'
 89         res =sum(array.array("H", data))
 90         res = (res >> 16) + (res & 0xffff)
 91         res += res >> 16
 92         return (~res) & 0xffff
 93 
 94 tcp_chk = checksum(ps_hdr)
 95 
 96 # Pack the tcp header to fill in the correct checksum - remember checksum is NOT in network byte order
 97 tcp_hdr = pack('!HHLLBBH', tcp_src, tcp_dst, tcp_seq, tcp_ack_seq, tcp_off_res, tcp_flags, tcp_win) + pack('H', tcp_chk) + pack('!H', tcp_urg_ptr)
 98 
 99 
100 #Combine all the headers and the use data
101 packet = ip_header + tcp_hdr + user_data
102 
103 # Send the Packet
104 s.sendto(packet, (dst_ip, 0))
sudo
