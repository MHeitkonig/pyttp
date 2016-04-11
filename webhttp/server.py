"""HTTP Server

This module contains a HTTP server
"""

import threading
#import socket
from socket import *
import parser
import message

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

    def handle_connection(self):
        """Handle a new connection"""
        print "[L>] ConnectionHandler/handle_connection"
        conn, addr = self.conn_socket.accept()
        print "Connected to: " + addr[0] + ":" + str(addr[1])
        requests = conn.recv(1024)
        print str(requests)
        p = parser.RequestParser()
        m = message.Request()
        parsed = p.parse_requests(requests)
        print "[L>] --- begin parsed --- "
        t = parsed[0]
        print "Method = " + t.get_header("Method:")
        print "URI = " + t.get_header("URI:")
        print "Version = " + t.get_header("Version:")
        print "Accept-Encoding = " + t.get_header("Accept-Encoding:")
        print "Host = " + t.get_header("Host:")
        print "Connection = " + t.get_header("Connection:")
        print "User-Agent = " + t.get_header("User-Agent:")
        print "[L>] ---- end parsed ---- "
        r = parser.ResponseParser()
        response = r.parse_response(t)
        print "\n[L>] --- begin response --- "
        print response
        print "[L>] ---- end response ----"
        conn.send()
        conn.close()
        pass

    def run(self):
        print "[L>] ConnectionHandler/run"
        self.handle_connection()


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
        conn_socket.bind((self.hostname, self.server_port))
        conn_socket.listen(5)
        print ("\tServer/run(self)//conn_socket.listen(1)")
        ch = ConnectionHandler(conn_socket, self.hostname, self.timeout)
        ch.start()
        while not self.done:
            pass

    def shutdown(self):
        """Safely shut down the HTTP server"""
        self.done = True
