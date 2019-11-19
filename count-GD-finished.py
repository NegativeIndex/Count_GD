#!/usr/bin/env python
import os,glob,sys
import re
import fnmatch
from optparse import (OptionParser,BadOptionError,AmbiguousOptionError)
import subprocess

##############################
# a wrapped class which passes all unknown option to args
class PassThroughOptionParser(OptionParser):
    """
    An unknown option pass-through implementation of OptionParser.

    When unknown arguments are encountered, bundle with largs and try again,
    until rargs is depleted.  

    sys.exit(status) will still be called if a known argument is passed
    incorrectly (e.g. missing arguments or bad argument types, etc.)        
    """
    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self,largs,rargs,values)
            except (BadOptionError,AmbiguousOptionError) as e:
                largs.append(e.opt_str)


#########################
def read_fb_file(fb_fname):
    n_sim=None
    with open(fb_fname) as fp:  
        for cnt, line in enumerate(fp):
            mobj=re.search('There are (\d+) simulations in this folder',line)
            if mobj:
                n_sim=int(mobj.group(1))
                break
    return n_sim

def read_fb_files():
    n_sim=None
    fb_fname=glob.glob('fb*txt')
    for fname in fb_fname:
        n_sim=read_fb_file(fname)
        if n_sim:
            # print('{}'.format(n_sim))
            break
    return n_sim
            
#########################
def check_RawData():
    n_finished=None
    if os.path.isdir("RawData"):
        # n_finished=int(len(glob.glob("RawData/*.txt"))/3)
        n_finished=len(fnmatch.filter(os.listdir('RawData'),'*.txt'))/3
        n_finished=int(n_finished)
        # print(n_finished)
    return n_finished
    
def process_a_folder(folders):
    # print(path)
    # folders=[os.path.abspath(x[0]) for x in os.walk(path)]
    folders.sort()
    folders=[os.path.abspath(folder) for folder in folders]
    [print(folder) for folder in folders]
    print('Total folders is {}'.format(len(folders)))
    sys.stdout.flush()
    jobs_todo=0
    jobs_done=0
    for folder in folders:
        os.chdir(folder)
        sys.stdout.flush()	
 
        n_sim=read_fb_files()
        n_finished=check_RawData()
        if (n_sim is not None) and (n_finished is not None):
            # print('-'*30)
            # print(os.getcwd())
            if (n_finished==n_sim):
                # print('{}/{}; Finished'.format(n_finished,n_sim))
                jobs_done+=n_finished
                jobs_todo+=n_sim-n_finished
            else:
                print('-'*30)
                print(os.getcwd())
                print('{}/{}'.format(n_finished,n_sim))
                jobs_done+=n_finished
                jobs_todo+=n_sim-n_finished
            sys.stdout.flush()
                
    print('='*30)
    if jobs_todo>0:
        print('{} jobs to do, {} finished'.format(jobs_todo,jobs_done))
    else:
        print('All {} the simulations are finished'.format(jobs_done))

#########################
# main function
str1='Usage: %prog <dir> '
str2='-maxdepth <int> '
str3='-name <string'
str4='This function passes all the options to find function '
str5='to list all appropriate folders.'
parser = PassThroughOptionParser(usage=str1+str2+str3,
                                 description=str4+str5)
# parser = OptionParser()
sargs=sys.argv
(options,args) = parser.parse_args()
# print(options)
# print(args)
# print(sargs)
    
# find all the folders which contains simulations
comm=["find"]+sargs[1:]+['-type','d']
res = subprocess.check_output(comm).decode("ascii").rstrip()
# print(args)
folders=res.split('\n')
process_a_folder(folders)


