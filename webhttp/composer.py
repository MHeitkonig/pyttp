""" Composer for HTTP responses

This module contains a composer, which can compose responses to
HTTP requests from a client.
"""

import time
import md5
import StringIO
import gzip
import webhttp.message
import webhttp.resource
import os


class ResponseComposer:
    """Class that composes a HTTP response to a HTTP request"""

    def __init__(self, timeout):
        """Initialize the ResponseComposer

        Args:
            timeout (int): connection timeout
        """
        self.timeout = timeout

    def compose_response(self, request):
        """Compose a response to a request

        Args:
            request (webhttp.Request): request from client

        Returns:
            webhttp.Response: response to request

        """
        response = webhttp.message.Response()

        # Stub code
        response.code = 500
        response.set_header("Version", "HTTP/1.1")

        #response.set_header("Connection", "keep-alive")
        resource = request.get_header("URI")

        response.body = ""

        contentdir = str(os.getcwd()) + "/content/"
        #print contentdir

        if len(resource) == 1 and resource[0] == "/":
            resource = "index.html"
        else:
            if resource[-1] == "/":
                resource = resource + "index.html"
                #print "loglog " + resource

        absolute_path = contentdir + resource
        status_dir = contentdir + "status/"
        if os.path.isfile(absolute_path):
            if os.access(absolute_path, os.R_OK): # Race condition, I know
                response.code = 200
            else:
                response.code = 403
        else:
            response.code = 404

        if response.code != 200:
            status_file = status_dir + str(response.code) + ".html"
            if os.path.isfile(status_file) and os.access(status_file, os.R_OK):
                response.body=open(status_file, "r").read()
            else:
                print ("[!] No custom error page found for " + str(response.code) + ", using hardcoded default")
                response.body = "<html>\n\t<head>\n\t\t<title>" + str(response.code) + "</title>\n\t</head>\n\t<body>\n\t\t<center>\n\t\t\t<h1>" + str(response.code) + " - " + response.get_reason(response.code) + "</h1>\n\t\t</center>\n\t</body>\n</html>"

        else:
            document = open(absolute_path, "r")
            response.body = document.read()

            
        if "gzip" in request.get_header("Accept-Encoding"):
            response.set_header("Content-Encoding", "gzip")
            out = StringIO.StringIO()
            with gzip.GzipFile(fileobj=out, mode="w") as f:
                f.write(str(response.body))
            response.body = out.getvalue()

        m = md5.new() # Not concerned about collision attacks here
        m.update(response.body)
        #digest = m.hexdigest()
        response.set_header("ETag", m.hexdigest())
        response.set_header("Date", self.make_date_string())
        response.set_header("Content-Length", len(response.body))
        return response

    def make_date_string(self):
        """Make string of date and time

        Returns:
            str: formatted string of date and time
        """
        return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())






























# Because I don't have a monitor stand and scrolling past code doesn't work in Atom
