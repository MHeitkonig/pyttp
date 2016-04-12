"""HTTP response and request parsers

This module contains parses for HTTP response and HTTP requests.
"""

import webhttp.message
import re
import os

class RequestParser:
    """Class that parses a HTTP request"""

    def __init__(self):
        """Initialize the RequestParser"""
        pass

    def parse_requests(self, buff):
        """Parse requests in a buffer

        Args:
            buff (str): the buffer contents received from socket

        Returns:
            list of webhttp.Request
        """
        requests = self.split_requests(buff)

        http_requests = []
        for request in requests:
            req = webhttp.message.Request()
            firstline = request.split('\n')[0]
            (method, uri, version) = firstline.split()
            req.set_header("Method", method)
            req.set_header("URI", uri)
            req.set_header("Version", version)
            remaining_headers = re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", request)
            # Thanks to https://bt3gl.github.io/black-hat-python-infinite-possibilities-with-the-scapy-module.html
            c = 0
            while c < len(remaining_headers):
                req.set_header(remaining_headers[c][0], remaining_headers[c][1])
                c += 1
            http_requests.append(req)
        return http_requests

    def split_requests(self, buff):
        """Split multiple requests

        Arguments:
            buff (str): the buffer contents received from socket

        Returns:
            list of str
        """
        requests = buff.split('\r\n\r\n')
        requests = filter(None, requests)
        requests = [r + '\r\n\r\n' for r in requests]
        requests = [r.lstrip() for r in requests]
        return requests

class ResponseParser:
    """Class that parses a HTTP response"""
    def __init__(self):
        """Initialize the ResponseParser"""
        pass

    def parse_response(self, parsedRequests):
        """Parse responses in buffer

        Args:
            buff (str): the buffer contents received from socket

        Returns:
            webhttp.Response
        """
        response = webhttp.message.Response()
        response.set_header("Version", "HTTP/1.1")
        return ""





































#because Atom won't let me scroll down and I don't have a monitor stand
