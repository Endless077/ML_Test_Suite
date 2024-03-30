# Utils
import os
import sys
from datetime import datetime as dt

# Logging Class
class Logger(object):
    def __init__(self, file=None, dir=None):
        if file is not None and dir is not None:
            if not isinstance(file, str) or not isinstance(dir, str):
                self.write("Logging", "Error: File name and directory must be strings.")
                self.log = None
            elif any(c in r'\/:*?"<>|' for c in file):
                self.write("Logging", "Error: File name contains invalid characters.")
                self.log = None
            else:
                if not os.path.exists(f"./{dir}"):
                    os.mkdir(f"./{dir}")
                curr_date = dt.now().isoformat().replace(':', '-')
                self.log = open(f"./{dir}/{file}_{curr_date}.txt", "x")
        else:
            self.log = None

    def write(self, tag, text):
        curr_time = dt.now().strftime("%H:%M:%S")
        log_message = f"[{tag} - {curr_time}] {text}\n"
        sys.stdout.write(log_message)
        
        if self.log:
            self.log.write(log_message)
        
    def flush(self):
        if self.log:
            self.log.flush()