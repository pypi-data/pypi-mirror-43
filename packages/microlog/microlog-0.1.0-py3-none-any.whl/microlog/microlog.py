#!/usr/bin/env python

import platform
import math
from datetime import datetime, timezone

class Logger():
    def __init__(self, file=False, console=True, ts=False):
        self._ts = ts
        self.__file = file
        self._logs = []
        self.__console = console

        if file == True:
            if platform.system() == "Windows": # Replace colons in filename if Windows
                self.__filename = self._time().replace(":","_")
            else:
                self.__filename = self._time()
        elif isinstance(self.__file, str):
            self.__filename = self.__file
        else:
            self.__filename = None

        if self.__file:
            file = open("{}.log".format(self.__filename),"a+")
            file.close()

    # Calculate datetime or timestamp for filename and/or log messages
    def _time(self):
        dt = datetime.now()
        if not self._ts:
            dt = dt.strftime('%Y-%m-%d %H:%M:%S')
            return dt
        else:
            ts = math.floor(dt.replace(tzinfo=timezone.utc).timestamp())
            return ts

    # Write log messages to the consol, log file, and/or memory
    def _write(self, line):
        if self.__console:
            print(line)
        if self.__file:
            file = open("{}.log".format(self.__filename), "a")
            file.write("{}\n".format(line))
            file.close()
        self._logs.append(line)

    # Toggle log messages appearing in the console (on by default)
    def console(self, state):
        if isinstance(state, bool):
            self.__console = state
        return self.__console

    # Return the last n logs (all by default)
    def logs(self, n=0):
        return self._logs[-n:]

    # Write a generic log message
    def log(self, message):
        ts = self._time()
        self._write("{ts} {msg}".format(ts=ts, msg=message))

    # Write a level specific log message
    def _base(self, level, message):
        ts = self._time()
        self._write("{ts} [{lvl}]: {msg}".format(ts=ts, msg=message, lvl=level))
    def debug(self, message):
        self._base("DEBUG", message)
    def info(self, message):
        self._base("INFO", message)
    def warning(self, message):
        self._base("WARNING", message)
    def error(self, message):
        self._base("ERROR", message)
    def critical(self, message):
        self._base("CRITICAL", message)
