import random
from datetime import datetime
import sys
import re

# assign client ID
def assign_client_id():
    today = "".join([
        str(datetime.today().month),
        str(datetime.today().day),
        str(datetime.today().year)[2:]
    ])
    id = "".join([
        str(random.randint(0, 10)) for i in range(0, 4)
    ])
    return "".join(['User', today, id])

# function to print welcome message for client
def print_welcome(name):
    welcome_msg = f"""
    Welcome, {name}!
    
    You're connected with a professional statistician.
    """
    print(welcome_msg)

# logging
def open_log(name, config):
    dt = datetime.now()
    timestamp = f"{dt.month}-{dt.day}-{dt.year}"
    filename = f"chat_log_{name}_{timestamp}.txt"
    log_file = open(filename, 'w')
    
    class Tee:
        def __init__(self, *files):
            self.files = files
            self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        
        def write(self, data):
            # Write raw data to terminal
            self.files[0].write(data)
            self.files[0].flush()
            
            # Write cleaned data to log file
            if len(self.files) > 1:
                clean_data = self.ansi_escape.sub('', data)
                # Also remove carriage returns that aren't followed by newlines
                clean_data = clean_data.replace('\r\033[K', '')
                clean_data = clean_data.replace('\r', '\n')
                # Skip footer lines
                command_prefix = config['commands']['cmd_prefix']
                footer_text = f"Run {command_prefix}help to view the command palette"
                if "Run !help to view the command palette" not in clean_data:
                    self.files[1].write(clean_data)
                    self.files[1].flush()
        
        def flush(self):
            for f in self.files:
                f.flush()
    
    sys.stdout = Tee(sys.stdout, log_file)
    return log_file, filename

def close_log(log_file, log_filename):
    sys.stdout = sys.__stdout__  # Restore original stdout
    log_file.close()
    print(f"Session log saved to: {log_filename}")
    return None
