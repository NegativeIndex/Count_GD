#!/usr/bin/env python
""" Count the number of simulations finined in a folder. 

"""
import os,glob,sys
import re
import fnmatch
import subprocess
sys.path.append("/Users/wdai11/python-study")
from  MKJob_GD_Matlab.Optparse_Addon import *


#########################
def read_fb_file(fb_fname):
    """Return the total number of simulations covered by the folder from a
    fb file.

    The actual simulation is written by Matlab. The first part of the
    simulation code is to provide the total number of simulations the
    code will calculate. The function read the output the retrieve the
    information.

    Parameters
    -----------
    fb_name : string
      the name of a fb.*txt file

    Returns
    -----------
    int
      The number of simulaitons.

    """
    n_sim=None
    with open(fb_fname) as fp:  
        for cnt, line in enumerate(fp):
            mobj=re.search('There are (\d+) simulations in this folder',line)
            if mobj:
                n_sim=int(mobj.group(1))
                break
    return n_sim

def read_fb_files():
    """Find fb files in current folder and return the total number of
    simulations coverd by the current folder.

    """
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
if __name__=='__main__':

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


