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

            #message.set_header("Method", method)
            #message.set_header("URI", uri)
            #message.set_header("Version", version)
            firstline = request.split('\n')[0]
            #print str(firstline)
            (method, uri, version) = firstline.split()
            req.set_header("Method", method)
            req.set_header("URI", uri)
            req.set_header("Version", version)
            remaining_headers = re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", request)
            #print ">>>>>" + str(len(remaining_headers)) + "<<<<<<"
            #print str(remaining_headers)
            #print remaining_headers[0][0]
            #print remaining_headers[0][1]
            c = 0
            while c < len(remaining_headers):
                req.set_header(remaining_headers[c][0], remaining_headers[c][1])
                c += 1
            # Thanks to https://bt3gl.github.io/black-hat-python-infinite-possibilities-with-the-scapy-module.html

            #word_split = re.compile('\\S+').findall(request) # Thanks to: https://stackoverflow.com/questions/225337/how-do-i-split-a-string-with-any-whitespace-chars-as-delimiters
            # nvm doesn't work for parsing user agent and content encoding
            #http_request.set_header("Method:", word_split[0])
            #http_request.set_header("URI:", word_split[1])
            #http_request.set_header("Version:", word_split[2])
            '''
            index = 3
            while index < len(word_split):
                http_request.set_header(word_split[index], word_split[index+1])
                index = index + 2
            # probably reason for array index out of bounds in safari'''
            #combined = dict(req.items() + remaining_headers.items())
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
        for request in parsedRequests:
            if request.get_header("Method") == "GET":
                self.parse_get(request, response)

        response.set_header("Version", "HTTP/1.1")

        #if buff.get_header("URI") == "/index.html":
        #    response.set_header("Code", "200")
        #else:
        #    response.set_header("Code", "404")
        return ""





































#because Atom won't let me scroll down and I don't have a monitor stand
