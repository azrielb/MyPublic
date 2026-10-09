import git # requires "GitPython"
import os
import sys
from azriel import ask_yn, run_os_command, get_output_of_os_command


try:
    repo = git.repo.Repo('.', search_parent_directories=True)
except Exception as e:
    print(type(e),e)
    repo = git.repo.Repo(os.path.dirname(__file__), search_parent_directories=True)
    
os.chdir(repo.git.rev_parse("--show-toplevel"))
print("git dir:", repo.git_dir)
print("remote url:", repo.remote().url)
print()
run_os_command(f"git fetch --all --prune --prune-tags")
if run_os_command("git pull") != 0:
    if ask_yn("Do you want to push your branch?"):
        run_os_command(f"git push --set-upstream origin {repo.active_branch.name}")
for branch in repo.branches:
    if branch != repo.active_branch and not branch.name.startswith("claude/"):
        exit_code = run_os_command(f"git fetch origin {branch.name}:{branch.name}") #we use the command line interface for printing the information
        if exit_code != 0:
            if ask_yn("Do you want to delete this local branch?", False):
                run_os_command("git branch -D " + branch.name)
run_os_command("git status")
def get_main_branch(repo):
    try:
        ref = repo.git.symbolic_ref('refs/remotes/origin/HEAD')
        return ref.split('/')[-1]
    except Exception:
        pass
    try:
        output = repo.git.ls_remote('--symref', 'origin', 'HEAD')
        for line in output.splitlines():
            if line.startswith('ref: refs/heads/'):
                return line.split('refs/heads/')[1].split('\t')[0]
    except Exception:
        pass
    for name in ('main', 'master'):
        if any(b.name == name for b in repo.branches):
            return name
    return None

branch_to_merge = sys.argv[1] if len(sys.argv) > 1 else get_main_branch(repo)
if branch_to_merge and branch_to_merge != repo.active_branch.name:
    run_os_command("git merge --no-edit " + branch_to_merge)
if 'use "git push"' in repo.git.status():
    if ask_yn("Do you want to push your changes?"):
        run_os_command("git push")
