"""HTTP Server

This module contains a HTTP server
"""

import threading
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
        print "[Connected to: " + addr[0] + ":" + str(addr[1]) + "]"
        requests = conn.recv(1024)
        p = parser.RequestParser()
        m = message.Request()
        parsed = p.parse_requests(requests)
        t = parsed[0]
        r = composer.ResponseComposer(15)
        response = r.compose_response(t)
        conn.send(str(response))
        print addr[0] + ":" + str(addr[1]) + " requested " + t.get_header("URI") + "\t[" + str(response.code) + "]"
        print response.get_header("URI")
        if t.get_header("Connection") == "close":
            conn.close()
            print "[Closed connection: " + addr[0] + ":" + str(addr[1]) + " because the client requested it]"
        pass

    def run(self, conn, addr):
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
        conn_socket = socket(AF_INET, SOCK_STREAM)
        conn_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # To prevent needing to switch ports every crash
        conn_socket.bind((self.hostname, self.server_port))
        conn_socket.listen(5)
        while True:
            conn, addr = conn_socket.accept()
            ch = ConnectionHandler(conn_socket, self.hostname, self.timeout)
            threading.Thread(target = ch.run(conn, addr))


        while not self.done:
            pass

    def shutdown(self):
        """Safely shut down the HTTP server"""
        self.done = True
