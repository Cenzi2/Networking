# Networking

ssh -X student@10.50.25.115

net1_10@
password10

*GUNNY GERWING'S TRIED AND TRUE METHODOLOGY NOTES*

Recon Methodology
1. Host discovery (nmap, nc, ./scan.sh, ping sweep)
for i in [1..254] ; do (ping -c 1 192.168.1.$i | grep "bytes from" &) ;done
nmap -Pn (no ping) -T4 (SPEED) <ip/cidr or 192.168.0.1,30,55,70> -p 21-23 80 | egrep -i "scan report|open"

2. Port/service discovery (nmap, nc, ./scan.sh)
scan for 21,22,23 and 80 first

3. Port validation (use netcat for banner grabbing)

4. Follow-on Actions based on ports found
4a. if it is ports 22-23, connect to it and do passive recon
4b. if it is ports 21 or 80, wget -r http://<ip> -or- wget -r ftp://<ip> (PULL THE FILES)

Scanning Methodology
1. Quick scan ports 21-23, 80 (if these ports dont exist, we dont care)
2. Scan specific ports based on hints/clues found
3. Well known ports: 1-1023
4. scan ports 1-10000
5. scan ALL ports :(

Passive Recon Methodology
hostname
ip addr, ifconfig (interfaces and subnets)
arp -a, ip neigh = Neighbors? (we dont care about the fail lines) ip neigh | egrep -iv "failed"
netstat/ss -nltp4 (Other listening ports? Filtered?)
ls /usr/cctc/share (Files of interest) (use the find command)
which tcpdump wireshark nmap telnet wget curl (which <command> check to see if the commands exist)
function enum () {
	hostname
	ip addr
	ip neigh
	ss -nltp4
	ls /usr/cctc/share
	which tcpdump wireshark nmap telnet wget curl
}
	
