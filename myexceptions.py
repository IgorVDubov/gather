class BaseException(Exception):
    """ Base exception """

    def __init__(self, string):
        """ Initialize the exception
        :param string: The message to append to the error
        """
        self.string = string

    def __str__(self):
        return 'Modbus Error: %s' % self.string

    def isError(self):
        """Error"""
        return True

class ChannelException(BaseException):
    """ Error executing channel """

    def __init__(self, string="", function_code=None):
        """ Initialize the exception
        :param string: The message to append to the error
        """
        self.fcode = function_code
        self.message = "[Input/Output] %s" % string
        BaseException.__init__(self, self.message)

class SourceException(BaseException):
    """ Error resulting from data source """

    def __init__(self, string="", function_code=None):
        """ Initialize the exception
        :param string: The message to append to the error
        """
        self.fcode = function_code
        self.message = "[Input/Output] %s" % string
        BaseException.__init__(self, self.message)


class ModbusException(SourceException):
    """ Error resulting from Modbus data i/o """

    def __init__(self, string="", function_code=None):
        """ Initialize the exception
        :param string: The message to append to the error
        """
        self.fcode = function_code
        self.message = "[Input/Output] %s" % string
        SourceException.__init__(self, self.message)
