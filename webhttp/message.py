"""HTTP Messages

This modules contains classes for representing HTTP responses and requests.
"""

reasondict = {
    # Dictionary for code reasons
    # Format: code : "Reason"
    200 : "OK",
    304 : "Not Modified",
    403 : "Forbidden",
    404 : "Not Found",
    406 : "Not Acceptable",
    418 : "I'm A Teapot",
    500 : "Internal Server Error"

}


class Message(object):
    """Class that stores a HTTP Message"""

    def __init__(self):
        """Initialize the Message"""
        self.version = "HTTP/1.1"
        self.startline = ""
        self.body = ""
        self.headerdict = dict()

    def set_header(self, name, value):
        """Add a header and its value

        Args:
            name (str): name of header
            value (str): value of header
        """
        self.headerdict[name] = value

    def get_header(self, name):
        """Get the value of a header

        Args:
            name (str): name of header

        Returns:
            str: value of header, empty if header does not exist
        """
        if name in self.headerdict:
            return self.headerdict[name]
        else:
            return ""

    def __str__(self):
        """Convert the Message to a string

        Returns:
            str: representation the can be sent over socket
        """

        return ""

    def get_reason(self, code):
        return reasondict[code]


class Request(Message):
    """Class that stores a HTTP request"""

    def __init__(self):
        """Initialize the Request"""
        super(Request, self).__init__()
        self.method = self.get_header("status")
        self.uri = ""

    def __str__(self):
        """Convert the Request to a string

        Returns:
            str: representation the can be sent over socket
        """
        message = self.get_header("Method") + " " + self.get_header("URI") + " " + self.get_header("Version") + "\r\n"
        if self.get_header("Host") != "":
            message += self.get_header("Host") + "\r\n"
        if self.get_header("User-Agent") != "":
            message += self.get_header("User-Agent") + "\r\n"
        if self.get_header("Accept") != "":
            message += self.get_header("Accept") + "\r\n"
        if self.get_header("Accept-Language") != "":
            message += self.get_header("Accept-Language") + "\r\n"
        if self.get_header("Accept-Encoding") != "":
            message += self.get_header("Accept-Encoding") + "\r\n"
        if self.get_header("DNT") != "":
            message += self.get_header("DNT") + "\r\n"
        if self.get_header("Connection") != "":
            message += self.get_header("Connection") + "\r\n"
        message += "\n"

        return message


class Response(Message):
    """Class that stores a HTTP Response"""

    def __init__(self):
        """Initialize the Response"""
        super(Response, self).__init__()
        self.code = 500

    def __str__(self):
        """Convert the Response to a string

        Returns:
            str: representation the can be sent over socket
        """
        message  = self.get_header("Version") + " " + str(self.code) + " " + reasondict[self.code] + "\r\n"
        message += "Date: " + str(self.get_header("Date")) + "\r\n"
        #message += "Content-Type: " + "text/html" + "\r\n" # todo!
        if (self.get_header("Content-Encoding") != ""):
            message += "Content-Encoding: " + str(self.get_header("Content-Encoding")) + "\r\n"
        message += "Content-Length:" + str(self.get_header("Content-Length")) + "\r\n"
        message += "ETag: " + str(self.get_header("ETag")) + "\r\n"
        message += "Connection: " + self.get_header("Connection") + "\r\n"
        message += "\n"
        message += self.body
        #print(message)
        return message
