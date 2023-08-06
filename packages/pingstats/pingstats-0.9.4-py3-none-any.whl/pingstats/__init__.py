""" Example Usage:

    >>> import pingstats
    >>> pings = pingstats.Pings('google.ca')
    >>> for ping in pings:
    ...     pingstats.plot_pings(pings.realtime_data)
    # HIPSTERPLOT OUTPUT
    ...     print(ping)
    # The most recent return time in milliseconds
"""
from __future__ import print_function, with_statement

# STANDARD LIBRARY PACKAGES
from subprocess import Popen, PIPE
from argparse import ArgumentParser
from os import name
import sys


# NON STANDARD LIBRARY PACKAGES
from hipsterplot import plot
from .config import get_lines, append_argv, parse_lines

# RUN CONFIG
if sys.argv[0].count('pingstats') and not sys.argv[0].count('.py'):
    lines = get_lines()
    if lines is not None:
        try:
            append_argv(parse_lines(lines))
        except AssertionError as e:
            print(str(e))
            exit(1)


__version__ = "0.9.4"
PROG_NAME = 'pingstats'

# PARSER CONFIG
parser = ArgumentParser(prog=PROG_NAME)

parser.add_argument('address', help='The address to ping. This could be either '
                    'a web address (i.e, "google.ca") or an IP address.')

parser.add_argument('-V', '--version', action='version',
                    version='%(prog)s {}'.format(__version__))

X_COLUMN_SCALE = 11 if name != 'nt' else 13
Y_ROW_SCALE = 0

# __all__ = ['Pings', 'plot_pings']


class Pings:
    """ Main logic object for obtaining ping data.

    Example Usage:
        >>> from pingstats import Pings
        >>> pings = Pings('127.0.0.1')
        >>> for this_time in pings:
        ...     print(pings.realtime_data)
        ...     print(pings.average_data)
        ...     print(pings.current_line)
        ...     print(this_time)  # current ping's realtime data in milliseconds
    """
    def __init__(self, address, realtime_data=[], average_data=[], realtime_data_length=20, average_data_length=200):
        """ Instantiates data used during the ping retrieval process.

        :address: The address to send ICMP ECHO requests to.
        :realtime_data: A python list object to continue to append data to.
        :average_data: A python list object to continue to append data to.
        :realtime_data_length: The maximum size of the realtime_data list
        :average_data_length: The maximum size of the average_data list
        """

        # NOTE: Must create data copy of argument lists to ensure new instances
        # have new lists.

        self.address = address
        self.realtime_data, self.average_data = realtime_data[:], average_data[:]
        self._realtime_data_length, self._average_data_length = realtime_data_length, average_data_length
        self.current_line = ''

    def _decode_line(self, line):
        """ Decodes a line from internal ping call, returning the connection time.

        ..note: This function also correctly handles switching between POSIX
                standard ``ping.c`` and Windows NT ``ping.c`` formats.

        :line: A line returned from `get_ping.process`.
        :returns: Either the return time in milliseconds (as float), -1 on timeout,
                or None.
        """
        if line.lower().count('ttl'):
            if name != "nt":
                return float(line.split('time=')[1].split(' ')[0])
            else:
                if line.count('time<'):
                    return float(line.split('time<')[1].split(' ')[0].strip('<ms'))
                else:
                    return float(line.split('time=')[1].split(' ')[0].strip('ms'))

        elif line.lower().count('0 received' if name != 'nt' else '100% loss'):
            return -1

    def _run_subprocess(self, address):
        """ Runs a ping subprocess, passing the user specified address to the command.

        ..note: This function also correctly handles switching between POSIX standard ``ping.c``
                and Windows NT ``ping.c`` formats.

        :address: The address to request ``ICMP ECHO`` requests to (i.e 'google.ca')
        :returns: The output of the sub process (POSIX standard or Windows NT ping output)
        """
        if name != 'nt':
            process = Popen(['ping', '-c 1', address], stdout=PIPE)
        else:
            process = Popen(['ping', '-n', '1', address], stdout=PIPE)

        process.wait()
        stdout, stderr = process.communicate()
        return stdout.decode('UTF-8').splitlines()

    def __iter__(self):
        """ Iteratively spawns ``ICMP`` requests for ``self.address``.

        :yields: The return time in milliseconds
        """
        # init data
        this_time = 0
        while 1:

            for line in self._run_subprocess(self.address):
                if len(self.realtime_data) > self._realtime_data_length:  # enforce max length
                    self.realtime_data.pop(0)

                line_value = self._decode_line(line)  # get float return length from line

                if line_value is not None:
                    this_time = line_value
                    self.current_line = line
                    self.realtime_data.append(line_value)

            else:  # On end of for loop, calculate average and append it
                if len(self.average_data) == self._average_data_length:
                    self.average_data.pop(0)

                self.average_data.append(sum(self.realtime_data) / len(self.realtime_data if self.realtime_data != 0 else 1))

            yield this_time


def get_pings(address):  # TODO Needs additional Testing
    """ Yields the last set of realtime and average data points, according to user
    specified maximum.

    :address: The address to send ``ICMP ECHO`` requests to.
    """
    pings = Pings(address)
    for ping in pings:
        yield pings.realtime_data[-1], pings.average_data[-1]


def plot_pings(pings, columns=70, rows=15):
    """ Provides high level bindings to ``hipsterplot.plot`` for use with :py:func:`pingstats.get_pings`.

    :pings: A list object containing ping return times as float values, normally from :py:func:`pingstats.get_pings`
    :columns: The number of columns to draw for the plot
    :rows: The number of rows to draw for the plot
    """
    plot(pings, num_x_chars=columns, num_y_chars=rows)
