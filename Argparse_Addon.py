#!/usr/bin/env python
"""
Some imporvements over the optparse module. The first part is to process unknown options; the second part is to process single dash long name.
"""

import argparse 
import logging
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


#########################
# main function
def main(argv):
    """A main function to implement the enhanced optparse_addon
    function. The function try to find job.info file in all the
    folders. The unknown options are passed to linux bash find
    function.

    I want to enforce a default vaule to -maxdepth option. I have to
    intercept the parser's help message.

    """
    # logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    str1='Usage: %prog <dir> '
    str2='-maxdepth <int> '
    str4='This function try to find job.info files and process them.'
    str5='It passes the unknown options to find function.'
    parser = PassThroughOptionParser(usage=str1+str2,
                                     description=str4+str5,
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # parser = OptionParser()
    # convert args help 
    # if args.help:
    #     help_string = parser.format_help()
    #     print(help_string.replace('--', '-'))
    #     parser.exit(0)

    # add some options
    parser.add_option("-u", "--unfinished",
                      action="store_true",
                      default=False,
                      help="Demonstrate unfinished folders.")

    parser.add_option("-s", "--summary",
                      action="store_true",
                      default=False,
                      help="Demonstrate only summary.")

    parser.add_option("-c", "--count",type=int, default=0,
                      help="Demonstrate the longest jobs.")


    parser.add_option("--maxdepth",type=int, default=1,
                      help="maximum search depth, default is 1")


    sargs=long_option_dash_1to2(argv)
    (opts,unk_args) = parser.parse_args(sargs)
    unk_args=long_option_dash_2to1(unk_args)

    # process unk_args
    unk_args.pop(0)  # remove the first, command name
    logging.debug("Saved args are {}".format(sargs))
    logging.debug("Accepted options is {}".format(opts))
    logging.debug("Unkonwn args are {}".format(unk_args))

    # find all the folders which contains simulations
    comm=["find"]+unk_args+['-name',"job.info"]
    res = subprocess.check_output(comm).decode("ascii").rstrip()
    # logging.debug(res)
    jobfiles=res.split('\n')
    jobfiles=[os.path.abspath(jobfile) for jobfile in jobfiles 
              if len(jobfile.strip())>0]

    jobfiles.sort()
    for f in jobfiles:
        logging.debug(f)


#########################
# main function
if __name__=='__main__':
    main(sys.argv)
