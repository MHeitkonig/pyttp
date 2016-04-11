from socket import *
import urllib2 as ul
ul.urlopen("http://localhost:8003/index.html").read()
#s = socket(AF_INET, SOCK_STREAM)
#s.connect(("localhost", 8001))
#s.send("Test")
#resp = s.recv(1024)
#print (str(resp))
