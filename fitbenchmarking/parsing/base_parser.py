"""
Implements the base Parser as a Context Manager.
"""

from abc import ABCMeta, abstractmethod


class Parser:
    """
    Base abstract class for a parser.
    Further parsers should inherit from this and override the abstract parse()
    method.
    """
    def __init__(self, filename):
        """
        Store the filename for use by enter.

        :param filename: The path to the file to be parsed
        :type filename: string
        """
        self._filename = filename
        self.file = None
        self.fitting_problem = None

    def __enter__(self):
        """
        Called when used as a context manager.
        Opens the file ready for parsing.
        """
        self.file = open(self._filename, 'r')

    def __exit__(self, type, value, traceback):
        """
        Called when used as a context manager.
        Closes the file.

        :param type: Used if an exception occurs. Contains the exception type.
        :type type: string?
        :param value: Used if an exception occurs. Contains the exception value.
        :type value: ?
        :param traceback: Used if an exception occurs. Contains the exception traceback.
        :type traceback: string?
        """
        if self.file is not None:
            self.file.close()

    @abstractmethod
    def parse(self):
        """
        Parse the file into a FittingProblem.

        :returns: The parsed problem
        :rtype: FittingProblem
        """
        raise NotImplementedError
