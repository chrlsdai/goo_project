import subprocess
import sys
import os
 
python_exe = sys.executable
target = os.path.join(sys.prefix, 'lib', 'site-packages')

subprocess.call([python_exe, '-m', 'ensurepip'])
subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'scipy', '-t', target])
 
print('FINISHED')
