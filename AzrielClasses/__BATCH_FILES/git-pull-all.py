import git # requires "GitPython"
import os
from azriel import ask_yn, run_os_command, get_output_of_os_command


try:
    repo = git.repo.Repo('.', search_parent_directories=True)
except Exception as e:
    print(type(e),e)
    repo = git.repo.Repo(os.path.dirname(__file__), search_parent_directories=True)
    
os.chdir(repo.git.rev_parse("--show-toplevel"))
if run_os_command("git pull") != 0:
    if ask_yn("Do you want to push your branch?"):
        run_os_command(f"git push --set-upstream origin {repo.active_branch.name}")
for branch in repo.branches:
    if branch != repo.active_branch:
        exit_code = run_os_command(f"git fetch origin {branch.name}:{branch.name}") #we use the command line interface for printing the information
        if exit_code != 0:
            if ask_yn("Do you want to delete this local branch?", False):
                run_os_command("git branch -D " + branch.name)            
run_os_command("git status")
if 'use "git push"' in repo.git.status():
    if ask_yn("Do you want to push your changes?"):
        run_os_command("git push")
