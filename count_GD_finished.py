#!/usr/bin/env python
""" Count the number of GD-Calc simulations finined in selected folders. 

"""
import os,glob,sys
import re
import fnmatch
import subprocess,logging
import argparse

# add sentences to help_string
def append_help_string(help_string, sentences=None):
    """Add some sentences at the end of the help_string. 

    Parameters
    -----------
    help_string : string
      the string return by parser.format_help()
    sentences: string list
      The sentences added at the end

    Returns
    -----------
    string
      The new version of help string

    """
    if sentences is not None:    
        help_string.rstrip()
        help_string=help_string[:-1]
        for line in sentences:
            help_string+='\n'+line
            help_string+='\n'

    return help_string

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
      The number of simulaitons; None if failed

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

    Returns
    -----------
    int
      The number of simulaitons coved by the current folder; None if failed
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
    """Count finished jobs in the current folder.

    Returns
    -----------
    int
      The number of finished simulaitons; 0 if failed
    """

    n_finished=0
    if os.path.isdir("RawData"):
        # n_finished=int(len(glob.glob("RawData/*.txt"))/3)
        n_finished=len(fnmatch.filter(os.listdir('RawData'),'*.txt'))/3
        n_finished=int(n_finished)
        # print(n_finished)
    return n_finished

#########################    
def process_folders(folders,args):
    """Count finished jobs in many folder. Print the results on screen
    based on the command line options.

    Parameters
    -----------
    folders:string list
      a list of folders which should contain simulations
    args: name space
      command line options

    Returns
    -----------
    No return
      Print the output on the screen based on args

    """    
    # print(path)
    # folders=[os.path.abspath(x[0]) for x in os.walk(path)]
    folders.sort()
    folders=[os.path.abspath(folder) for folder in folders]
    # print all the folders
    # [print(folder) for folder in folders]
    n_folder=len(folders)
    # print('Number of selected folders is {}'.format(n_folder))

    # sys.stdout.flush()
    n_fb=0  # number of folders with valud fb files
    n_finished=0 # number of finished folders
    jobs_todo=0
    jobs_done=0
    rpath=os.getcwd()
    # print switch
    opts=(args.bad, args.unfinished, args.finished)
    opts=list(opt or args.all for opt in opts)
    
    for folder in folders:
        os.chdir(folder)
        sys.stdout.flush()	
 
        cn_sim=read_fb_files()
        cn_finished=check_RawData()
        cpath=os.getcwd()
        os.chdir(rpath)
 
        # tags
        tags=(True,False,False)
        desc="No valid fb files"

        if (cn_sim is not None) :
            tags=(False,True,False)
            desc='{}/{} is done'.format(cn_finished,cn_sim)
            # print('-'*30)
            # print(os.getcwd())
            n_fb+=1
            jobs_done+=cn_finished
            jobs_todo+=cn_sim-cn_finished
            if (cn_finished==cn_sim):
                n_finished+=1
                tags=(False,False,True)
                desc='{}/{}; ALL DONE'.format(cn_finished,cn_sim)
            
        # print folder based on args
        if any(x and y for x,y in zip(opts,tags)):
            print('-'*30)
            print(cpath)
            print(desc)
    # always print summary
    print('='*30)
    print('{} folder selected; {} valid folders; {} finished'.format(
        n_folder,n_fb,n_finished))
    if jobs_todo>0:
        print('{:,} jobs to do, {:,} finished'.format(jobs_todo,jobs_done))
    else:
        print('All {:,} the simulations are finished'.format(jobs_done))

#######################
# main function
def main(argv):
    """The main function to find the simulation folders and count the
    finished jobs.

    I have to enforce a default vaule to -maxdepth option since the
    simulation folders contain too many small files.

    optional arguments:

      -p [PATH [PATH ...]], --path [PATH [PATH ...]]
                          Searching paths

      -b, --bad             Print the folders without a valid fb file.
      -u, --unfinished      Print the unfinished folders.
      -f, --finished        Print the finished folders.
      -a, --all             Print all the selected folders; 
                            equivalent to ``-buf``.
      -h, --help            Show this message and quit

      ``-maxdepth MAXDEPTH``   
        Maximum search depth, default is 1

      All the other unknown options will be passed to bash find command.


    """   
    # logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')
    # main function
    str4='This function findd the simulation folders'
    str5=' and count the finished jobs.'
    parser=argparse.ArgumentParser(add_help=False,
                                   description='\n'.join((str4,str5)) )
    
    # add some options
    parser.add_argument("-p","--path",
                      default=['./',], nargs='*',
                      help="Searching paths")

    parser.add_argument("-b", "--bad",
                        action="store_const",
                        const=True,
                        default=False,
                        help="Print the folders without a valid fb file.")

    parser.add_argument("-u", "--unfinished",
                        action="store_const",
                        const=True,
                        default=False,
                        help="Print the unfinished folders.")

    parser.add_argument("-f", "--finished",
                        action="store_const",
                        const=True,
                        default=False,
                        help="Print the finished folders.")

    parser.add_argument("-a", "--all",
                      action="store_true",
                      default=False,
                      help="Print all the selected folders. Equivalent to -buf")


    parser.add_argument("-maxdepth",type=int, default=1,
                      help="maximum search depth, default is 1")

    parser.add_argument('-h', '--help', 
                        help='Show this message and quit', 
                        action='count')

    ## process unknown options
    argv.pop(0)  # remove the first, command name
    args,unk_args=parser.parse_known_args(argv)

    if args.help:
        help_string = parser.format_help()
        sentences=('  All other long names with single dash '+
            'will be passed to bash find command.', )
        help_string=append_help_string(help_string,sentences)
        print(help_string)
        parser.exit(0)
    
    # find the folders to check
    comm=["find"]+args.path+['-maxdepth',str(args.maxdepth)]\
        +unk_args+['-type','d']
    res = subprocess.check_output(comm).decode("ascii").rstrip()
    # print(args)
    folders=res.split('\n')
    # for folder in folders:
    #     logging.debug(folder)
    process_folders(folders,args)


#########################
if __name__=='__main__':
    main(sys.argv)



