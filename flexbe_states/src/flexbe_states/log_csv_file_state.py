#!/usr/bin/env python
import os
import time
from flexbe_core import EventState, Logger


class LogCsvFileState(EventState):
    """
    A state that can write text into a file.  The current timestamp will be prepended with a semicolon.
    Additional userdata keys can be passed which will be appended with semicolons.

    -- text             string    Message which is written to the file.
    -- filepath         string    Absolute path to the logging file.
    -- additional_keys  string[]  Additional input keys which will be appended to message.
    -- log              bool      Log text in addition to writing into the file.
    -- severity         unit8     Severity of log.

    <= done                       Indicates that the message has been written.
    """

    def __init__(self, text, filepath="~/.flexbe_logs/log_file.csv", additional_keys=[], log=True, severity=Logger.REPORT_HINT):
        super(LogCsvFileState, self).__init__(outcomes=["done"], input_keys=additional_keys)
        self._filepath = filepath
        self._text = text
        self._additional_keys = additional_keys
        self._log = log
        self._severity = severity

    def execute(self, userdata):
        return "done"

    def on_enter(self, userdata):
        try:
            # Generate CSV string
            csv_string = self._text
            for key in self._additional_keys:
                csv_string += ";" + str(getattr(userdata, key))

            # Log
            if self._log:
                Logger.log(csv_string, self._severity)

            # Append to file with current timestamp
            with open(os.path.expanduser(self._filepath), "a") as file_object:
                file_object.write(str(time.time()) + ";" + csv_string + "\n")

        except Exception as ex:
            Logger.logerr(f"[LogCsvFileState] Exception: {ex}")
