import re
import subprocess
import sys
from azriel import run_os_command, get_output_of_os_command


def run_with_backticks(cmdline):
    ret = ''
    while True:
        match = re.search(r'`([^`]+)`', cmdline)
        if not match:
            break
        output = get_output_of_os_command(match.group(1).strip())
        ret += cmdline[:match.start()] + output 
        cmdline = cmdline[match.end():]
    return ret + cmdline

def main(argv):
    if len(argv) < 2:
        print(f"Usage: python {argv[0]} \"command with `cmd`\"")
        return 1
    return run_os_command(run_with_backticks(" ".join(sys.argv[1:])))

if __name__ == "__main__":
    sys.exit(main(sys.argv))
