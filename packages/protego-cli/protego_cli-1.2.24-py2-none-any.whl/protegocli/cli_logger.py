import logging
import sys

class CLILogger:
    def __init__(self, quiet, verbose):
        self._quiet = quiet
        self.__init_logger(verbose)

    def __init_logger(self, verbose):
        self._logger = logging.getLogger('FSP CLI TOOL')
        stream_handler = logging.StreamHandler()
        self._logger.addHandler(stream_handler)

        log_level = logging.getLevelName('INFO')
        if verbose:
            log_level = logging.getLevelName('DEBUG')

        self._logger.setLevel(log_level)

    def debug(self, msg):
        if self._quiet:
            return
        self._logger.debug('[FSP CLI TOOL][DEBUG]  ' + msg)

    def info(self, msg):
        if self._quiet:
            return
        self._logger.info(msg)

    def error(self, msg):
        if self._quiet:
            return
        self._logger.error('[FSP CLI TOOL][ERROR]  ' + msg)

    def warning(self, msg):
        if self._quiet:
            return
        self._logger.warning('[FSP CLI TOOL][WARNING]  ' + msg)

    def error_and_exit(self, msg):
        self.error(msg)
        sys.exit(1)

    def print_headline(self, msg):
        if self._quiet:
            return
        delim = "*"
        self._logger.info(delim * 100)
        self._logger.info(delim)
        self._logger.info(delim + " " + msg)
        self._logger.info(delim)
        self._logger.info(delim * 100)
