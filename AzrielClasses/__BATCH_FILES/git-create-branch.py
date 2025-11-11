import os
import sys
from azriel import ask_yn, run_os_command


if len(sys.argv) != 3:
    sys.exit("The input should contain only the path and the branch name (each in one word)!")
path = sys.argv[1]
branch_name = sys.argv[2]

os.chdir(path)
run_os_command("git status", True)

if not ask_yn(f"Do you want to create (locally and remotely) this branch [{branch_name}]?", False):
    sys.exit()

run_os_command("git checkout main", True)
run_os_command("git pull", True)
run_os_command(f"git checkout -b {branch_name}", True)
run_os_command(f"git push --set-upstream origin {branch_name}", True)
run_os_command("git status")
