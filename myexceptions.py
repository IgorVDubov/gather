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


class ModbusException(BaseException):
    """ Error resulting from data i/o """

    def __init__(self, string="", function_code=None):
        """ Initialize the exception
        :param string: The message to append to the error
        """
        self.fcode = function_code
        self.message = "[Input/Output] %s" % string
        ModbusException.__init__(self, self.message)
