from datetime import datetime

'''
	This file should contain functions that are commonly used in the cogs clients
'''

class terminal_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

async def print_message(message:str, error:str = '') -> None:
    c = datetime.now()
    time = c.strftime('%H:%M:%S')
    if error != '':
        print(f'{terminal_colors.FAIL} [{time}] {message} {terminal_colors.ENDC}')
    else:
        print(f'{terminal_colors.OKCYAN} [{time}] {message} {terminal_colors.ENDC}')