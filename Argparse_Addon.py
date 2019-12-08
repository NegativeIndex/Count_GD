#!/usr/bin/env python
"""
Some imporvements over the optparse module. The first part is to process unknown options; the second part is to process single dash long name.
"""

import argparse, logging
import sys,subprocess,os,re

############################
####
## convert long option with single dash to two dashes
def long_option_dash_1to2(args):
    """
    Change the sinlge-dash in front of a long option back to double-dash.
    """
    new_argv = []
    for arg in args:
        if arg.startswith('-') and len(arg) > 2:
            arg = '-' + arg
        new_argv.append(arg)
    return new_argv

# convert long option with two dashes to one
def long_option_dash_2to1(args):
    """
    Change the double-dash in front of a long option to single-dash.
    """
    new_argv = []
    for arg in args:
        arg = re.sub('^--','-',arg)
        new_argv.append(arg)
    return new_argv

# modify help string
def modify_help_string(help_string,longnames=None,sentences=None):
    """Modify the help_string. It receive a help_string, changes the double
    dash in front of some names to single dash, and add some sentences
    at the end.

    Parameters
    -----------
    help_string : string
      the string return by parser.format_help()
    longnames: string list
      The names with single dash
    sentences: string list
      The sentences added at the end

    Returns
    -----------
    string
      The new version of help string

    """
    if longnames is not None:
        for name in longnames:
            st1='--'+name
            st2='-'+name
            help_string=help_string.replace(st1, st2)

    if sentences is not None:    
        help_string.rstrip()
        help_string=help_string[:-1]
        for line in sentences:
            help_string+='\n'+line
            help_string+='\n'

    return help_string


#########################
# main function
def main(argv):
    """A main function to demonstrate the funciton argparse_addon
    function. The function try to find some files and process them.
    The unknown options are passed to linux bash find function.

    I want to enforce a default vaule to -maxdepth option. I have to
    intercept the parser's help message.

    Usage: Argparse_Addon.py [-p [PATH [PATH ...]]] [-s] [-maxdepth MAXDEPTH] [-h]

    optional arguments:
  
      -p [PATH [PATH ...]], --path [PATH [PATH ...]]     
                           Searching paths

      -s, --summary         Demonstrate only summary

      -h, --help            Show this message and quit

    option modification:
    
      ``-maxdepth MAXDEPTH``    
          maximum search depth, default is 1

      All other long names with single dash will be passed to bash find command.

    """
    # logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    str4='This function try to find some files and process them.'
    str5='It passes the unknown options to find function.'
 
    # intercept help
    parser=argparse.ArgumentParser(add_help=False,
                                   description='\n'.join((str4,str5)) )
    # parser=argparse.ArgumentParser(description='\n'.join((str4,str5)) )

    # add some options
    parser.add_argument("-p","--path",
                      default=['./',], nargs='*',
                      help="Searching paths")


    parser.add_argument("-s", "--summary",
                      action="store_true",
                      default=False,
                      help="Demonstrate only summary.")

    parser.add_argument("--maxdepth",type=int, default=1,
                      help="maximum search depth, default is 1")

    parser.add_argument('-h', '--help', 
                        help='Show this message and quit', 
                        action='count')

    ## process unknown options
    argv.pop(0)  # remove the first, command name
    # logging.debug("Before process are {}".format(argv))
    sargs=long_option_dash_1to2(argv)
    args,unk_args=parser.parse_known_args(sargs)
    unk_args=long_option_dash_2to1(unk_args)

    # process unk_args
    # logging.debug("Saved args are {}".format(sargs))
    # logging.debug("Accepted args is {}".format(args))
    # logging.debug("Unkonwn args are {}".format(unk_args))

    # new help documents
    if args.help:
        help_string = parser.format_help()
        sentences=('  All other long names with single dash '+
            'will be passed to bash find command.', )
        help_string=modify_help_string(help_string,('maxdepth',),
                                       sentences)
        print(help_string)
        parser.exit(0)

    # find files and list them
    comm=["find"]+args.path+['-maxdepth',str(args.maxdepth)]+unk_args
    res = subprocess.check_output(comm).decode("ascii").rstrip()
    print(res)
  


#########################
# main function
if __name__=='__main__':
    main(sys.argv)
