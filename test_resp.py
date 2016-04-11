from socket import *
s = socket(AF_INET, SOCK_STREAM)
s.connect(("localhost", 8001))
resp = s.recv(1024)
print (str(resp))
