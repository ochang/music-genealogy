import os
from subprocess import call


DIR = './gv'

os.chdir(DIR)
filelist = os.listdir('.')

for gv in filelist:
    path = os.path.abspath(gv)
    output_path = gv.split('.')[0] + '.png'

    call_args = ['twopi', '-Tpng', path, '-o', output_path]
    call(call_args)