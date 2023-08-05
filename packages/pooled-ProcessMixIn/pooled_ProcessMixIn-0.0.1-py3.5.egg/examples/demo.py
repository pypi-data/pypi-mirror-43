#!/usr/lib/env python3

import os
import time
import logging
from threading import currentThread
from multiprocessing import cpu_count
from pooledProcessMixin import PooledProcessMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyTestHandler (BaseHTTPRequestHandler):
    """

    Test Web application that outputs parent process id PPID, PID, thread, and URI and client address

    """
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        time.sleep(0.5)
        self.wfile.write(bytes(('PPID=[%d] PID=[%d] thread=[%s] uri=[%s] from [%s]' % (
            os.getppid(), os.getpid(), currentThread().name, self.path, self.client_address[0],)).encode()))
        if self.path == '/shutdown':
            print("testing software shutting down.")
            self.server.shutdown()
        

class MyHTTPTest (PooledProcessMixIn, HTTPServer):
    """

    Simple http-server

    """
    def __init__(self, processes=max(2, cpu_count()), threads=64, daemon=False, kill=True, debug=False, logger=None):
        """

        Constructor

        :param processes: processes pool length
        :type processes: int
        :param threads: threads pool length for process
        :type threads: int
        :param daemon: True if daemon threads
        :type daemon: bool
        :param kill: True if kill main process when shutdown
        :type kill: bool
        :param debug: True if debug mode
        :type debug: bool
        :param logger: logger
        :type logger: logging.Logger

        """
        HTTPServer.__init__(self, ('127.0.0.1', 8888), MyTestHandler)
        self._process_n = processes
        self._thread_n = threads
        self._daemon = daemon
        self._kill = kill
        self._debug = debug
        self._logger = logger
        self._init_pool()
        print("listening on http://127.0.0.1:8888/")

########################################################################################################################
#                                                    Entry point                                                       #
########################################################################################################################


if __name__ == '__main__':
    logging_format = '%(levelname)-10s|%(asctime)s|%(process)d|%(thread)d| ' \
                     '%(name)s --- %(message)s (%(filename)s:%(lineno)d)'
    logging.basicConfig(level=logging.INFO, format=logging_format)
    logger = logging.getLogger('default')
    handler = logging.FileHandler('/tmp/demo.log', encoding='utf8')
    handler.setFormatter(logging.Formatter(logging_format))
    logger.addHandler(handler)
    logger.setLevel(level=logging.DEBUG)
    test = MyHTTPTest(processes=2, threads=2, logger=logger)
    try:
        test.serve_forever()
    finally:
        test.shutdown()
    print("Done.")
