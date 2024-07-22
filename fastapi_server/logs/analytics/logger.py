# Logger Class
import os
import sys

from datetime import datetime as dt

class Logger(object):
    _instance = None
    _log = None
    
    def __new__(cls, filename=None, directory=None):
        if cls._instance is None:
            if filename is None or directory is None:
                raise ValueError("Filename and directory must be provided for the first initialization.")
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(filename, directory)
        return cls._instance

    def _initialize(self, filename=None, directory=None):
        if filename is not None and directory is not None:
            if not isinstance(filename, str) or not isinstance(directory, str):
                self.write("Logging", "Error: File name and directory must be strings.")
                self._log = None
            elif any(c in r'\/:*?"<>|' for c in filename):
                self.write("Logging", "Error: File name contains invalid characters.")
                self._log = None
            else:
                if not os.path.exists(f"{directory}"):
                    os.makedirs(f"{directory}")
                curr_date = dt.now().isoformat().replace(':', '-')
                self._log = open(f"{directory}/{filename}_{curr_date}.log", "x")
        else:
            self._log = None

    def write(self, tag, text):
        curr_time = dt.now().strftime("%H:%M:%S")
        log_message = f"[{tag} - {curr_time}] {text}\n"
        sys.stdout.write(log_message)
        
        if self._log is not None:
            self._log.write(log_message)
        
    def flush(self):
        if self._log is not None:
            self._log.flush()

###################################################################################################

def get_logging():
    if Logger._instance is None:
        filename = "logs"
        directory = "./logs"

        Logger(filename, directory)
    return Logger._instance
