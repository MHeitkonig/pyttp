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
            http_request = webhttp.message.Request()
            word_split = re.compile('\\S+').findall(request) # Thanks to: https://stackoverflow.com/questions/225337/how-do-i-split-a-string-with-any-whitespace-chars-as-delimiters
            http_request.set_header("Method:", word_split[0])
            http_request.set_header("URI:", word_split[1])
            http_request.set_header("Version:", word_split[2])

            index = 3
            while index < len(word_split):
                http_request.set_header(word_split[index], word_split[index+1])
                index = index + 2

            http_requests.append(http_request)
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

    def parse_response(self, buff):
        """Parse responses in buffer

        Args:
            buff (str): the buffer contents received from socket

        Returns:
            webhttp.Response
        """
        response = webhttp.message.Response()
        response.set_header("Version:", "HTTP/1.1")
        if buff.get_header("URI:") == "/index.html":
            response.set_header("StatusCode:", "200")
        else:
            response.set_header("StatusCode:", "404")
        return response
