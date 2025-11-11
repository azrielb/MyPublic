import os
import subprocess
import sys


if os.name == 'nt':
    os.system('') # thanks to ChatGPT that has given me this tip for using the coloring in `run_os_command`

def run_os_command(cmd, abort_for_any_error=False):
    print(f'\033[93m{cmd}\033[0m')
    exit_code = os.system(cmd)
    print()
    if abort_for_any_error and exit_code != 0:
        print(f"Error #{exit_code} has been occured!")
        sys.exit(exit_code)
    return exit_code

def get_output_of_os_command(cmd):
    try:
        return subprocess.check_output(cmd.split(), shell=True, text=True).strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command `{cmd}`:", e)
        raise(e)

def ask_yn(question, yes_is_default = True):
    options = '[Y]|[n]' if yes_is_default else '[y]|[N]'
    default_res = 'y' if yes_is_default else 'n'
    res = (input(f"{question} {options} ") or default_res)[0].lower()
    print()
    if yes_is_default:
        return res != 'n'
    return res == 'y'
    
if __name__ == "__main__":
    while ask_yn(""):
        pass
