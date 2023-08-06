"""
    A connection that reconnects smartly.
"""

import http.client
import logging
import socket
import time

from . import amp

DEFAULT_RECONNECT_TIMOUT = 10
DEFAULT_SOCKET_TIMOUT = 10


class SmartConn:
    """ A connection that reconnects smartly. """
    def __init__(self, logger, https, host, port, timeout=DEFAULT_SOCKET_TIMOUT,
                 reconnect_timeout=DEFAULT_RECONNECT_TIMOUT):
        logging.basicConfig()
        self.__conn = None
        self._disconnect_time = time.time()
        self._logger = logger or logging.getLogger('amp')
        self._https, self._host, self._port = https, host, port
        self._reconnect_timeout = reconnect_timeout
        self._socket_timeout = timeout
        self._c()
        if self._conn is None:
            raise amp.AmpError("Can't connect to %s:%s" % (host, port))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _c(self):
        if self._https:
            self._conn = http.client.HTTPSConnection(self._host, self._port, self._socket_timeout)
        else:
            self._conn = http.client.HTTPConnection(self._host, self._port, self._socket_timeout)
        try:
            self._conn.connect()
        except socket.error:
            self._logger.warning("Can't connect to %s:%d" % (self._host, self._port))
            self._conn.close()
            self._disconnect_time = time.time()
            self._conn = None

    def _r(self, method, path, data, headers):
        try:
            self._conn.request(method, path, data, headers)
        except ConnectionError:
            self._logger.warning("The connection to %s:%d has dropped" % (self._host, self._port))
            self._conn.close()
            self._disconnect_time = time.time()
            self._conn = None
            raise Exception("The connection to %s:%d has dropped" % (self._host, self._port))
        response = self._conn.getresponse()
        text = response.read()
        text = text.decode('utf-8')
        if response.status != 200:
            raise amp.AmpError('%s %s:%s/%s failed with status %d: %s' %
                               (method, self._host, self._port, path, response.status, text))
        return text

    def request(self, method, path, data=None, headers=None):
        """ Make a request to Amp agent. """
        if headers is None:
            headers = {}
        if self._conn is not None:
            return self._r(method, path, data, headers)
        if time.time() - self._disconnect_time < self._reconnect_timeout:
            raise Exception("The connection to %s:%d is down" % (self._host, self._port))
        self._c()
        if self._conn is None:
            raise Exception("The connection to %s:%d is down" % (self._host, self._port))
        return self._r(method, path, data, headers)

    def close(self):
        """ Close connection. """
        if self._conn is not None:
            self._conn.close()
