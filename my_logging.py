from datetime import datetime
from time import time
from tokenize import String

def log(msg, user = None):
    act_time = datetime.fromtimestamp(int(time()))

    if user:
        print(f'[{act_time}] [{user}] {msg}')
        return 
    
    print(f'[{act_time}] [Client] {msg}')

