"""
@author: Kudzai Tsapo (kudzai@charteredsys.com)

Description: 
--------------
This file contains the implementation for the errors raised by the library.
"""

class InvalidFileException(Exception):
    """
        This defines a custom exception that could occur when handling SQL Files.

        Parameters
        ----------
        arg : str
            The argument to pass when raising this exception
    """
    def __init__(self, arg):
        self.args = arg