import os
import subprocess
from azriel import run_os_command, get_output_of_os_command


output = get_output_of_os_command('python -m pip --disable-pip-version-check list --outdated')
print(output)
'''An example for the output:
Package    Version Latest       Type
---------- ------- ------------ -----
pyelftools 0.29    0.30         wheel
starlette  0.31.1  0.33.0       wheel
uvicorn    0.23.2  0.24.0.post1 wheel
'''
lines = output.split('\n')[2:]
packagesThatNeedToBeUpdatedAlways = 'pip'
packagesNames = [packageInfo.split()[0] for packageInfo in lines]
if packagesNames:
    run_os_command('python -m pip install --no-warn-script-location --upgrade ' + packagesThatNeedToBeUpdatedAlways + ' ' + ' '.join(packagesNames))
else:
    print("All relevant pip packages are up-to-date")