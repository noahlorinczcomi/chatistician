import random
from datetime import datetime
import shutil
import sys

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
