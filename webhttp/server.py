"""HTTP Server

This module contains a HTTP server
"""

import threading
#import socket
from socket import *
import parser
import message
import composer

class ConnectionHandler(threading.Thread):
    """Connection Handler for HTTP Server"""

    def __init__(self, conn_socket, addr, timeout):
        """Initialize the HTTP Connection Handler

        Args:
            conn_socket (socket): socket used for connection with client
            addr (str): ip address of client
            timeout (int): seconds until timeout
        """
        super(ConnectionHandler, self).__init__()
        self.daemon = True
        self.conn_socket = conn_socket
        self.addr = addr
        self.timeout = timeout

    def handle_connection(self, conn, addr):
        """Handle a new connection"""
        print "[L>] ConnectionHandler/handle_connection"
        #conn, addr = self.conn_socket.accept()
        print "Connected to: " + addr[0] + ":" + str(addr[1])
        requests = conn.recv(1024)
        print str(requests)
        p = parser.RequestParser()
        m = message.Request()
        parsed = p.parse_requests(requests)
        print "[L>] -M- begin parsed -M- "
        t = parsed[0]
        print "Method = " + t.get_header("Method")
        print "URI = " + t.get_header("URI")
        print "Version = " + t.get_header("Version")
        print "Accept-Encoding = " + t.get_header("Accept-Encoding")
        print "Host = " + t.get_header("Host")
        print "Connection = " + t.get_header("Connection")
        print "User-Agent = " + t.get_header("User-Agent")
        print "[L>] -M-- end parsed --M- "
        print "[L>] -A- begin parsed -A- "
        print str(parsed[0])
        print "[L>] -A-- end parsed --A- "
        #r = parser.ResponseParser()
        r = composer.ResponseComposer(15)
        #response = r.parse_response(t)
        #response1 = "HTTP/1.1 500 Internal Server Error\n\n"
        #response2 = "HTTP/1.1 404 Not Found\n\n"
        #msg = response1
        print "\n[L>] --- begin response --- "
        response = r.compose_response(t)
        print str(response)
        #print msg
        print "[L>] ---- end response ----"
        conn.send(str(response))
        conn.close()
        pass

    def run(self, conn, addr):
        print "[L>] ConnectionHandler/run"
        self.handle_connection(conn, addr)


class Server:
    """HTTP Server"""

    def __init__(self, hostname, server_port, timeout):
        """Initialize the HTTP server

        Args:
            hostname (str): hostname of the server
            server_port (int): port that the server is listening on
            timeout (int): seconds until timeout
        """
        self.hostname = hostname
        self.server_port = server_port
        self.timeout = timeout
        self.done = False

    def run(self):
        """Run the HTTP Server and start listening"""
        print ("[L>] Server/run(self)") # debug
        conn_socket = socket(AF_INET, SOCK_STREAM)
        conn_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # because I had to switch ports on every crash
        conn_socket.bind((self.hostname, self.server_port))
        conn_socket.listen(5)
        print ("\tServer/run(self)//conn_socket.listen(1)")
        while True:
            conn, addr = conn_socket.accept()
            ch = ConnectionHandler(conn_socket, self.hostname, self.timeout)
            threading.Thread(target = ch.run(conn, addr))


        while not self.done:
            pass

    def shutdown(self):
        """Safely shut down the HTTP server"""
        self.done = True
