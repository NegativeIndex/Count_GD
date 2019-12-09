MKJob_GD_Matlab
***************

Several programs to manage Matlab simulations using GD-Calc package.


Description
===========
Welcome to MKJob_GD_Matlab's documentation!
*******************************************


Aptparse_Addon module
=====================

Some imporvements over the optparse module. The first part is to
process unknown options; the second part is to process single dash
long name.

Count_GD.Argparse_Addon.long_option_dash_1to2(args)

   Change the sinlge-dash in front of a long option back to double-
   dash.

Count_GD.Argparse_Addon.long_option_dash_2to1(args)

   Change the double-dash in front of a long option to single-dash.

Count_GD.Argparse_Addon.main(argv)

   A main function to demonstrate the funciton argparse_addon
   function. The function try to find some files and process them. The
   unknown options are passed to linux bash find function.

   I want to enforce a default vaule to -maxdepth option. I have to
   intercept the parser's help message.

   Usage: Argparse_Addon.py [-p [PATH [PATH ...]]] [-s] [-maxdepth
   MAXDEPTH] [-h]

   optional arguments:

      -p [PATH [PATH ...]], --path [PATH [PATH ...]]
         Searching paths

      -s, --summary

      Demonstrate only summary

      -h, --help

      Show this message and quit

   option modification:

      "-maxdepth MAXDEPTH"
         maximum search depth, default is 1

      All other long names with single dash will be passed to bash
      find command.

Count_GD.Argparse_Addon.modify_help_string(help_string, longnames=None, sentences=None)

   Modify the help_string. It receive a help_string, changes the
   double dash in front of some names to single dash, and add some
   sentences at the end.

   Parameters:
      * **help_string** (*string*) -- the string return by
        parser.format_help()

      * **longnames** (*string list*) -- The names with single dash

      * **sentences** (*string list*) -- The sentences added at the
        end

   Returns:
      The new version of help string

   Return type:
      string


count_GD_finished module
========================

Count the number of GD-Calc simulations finined in selected folders.

Count_GD.count_GD_finished.check_RawData()

   Count finished jobs in the current folder.

   Returns:
      The number of finished simulaitons; 0 if failed

   Return type:
      int

Count_GD.count_GD_finished.main(argv)

   The main function to find the simulation folders and count the
   finished jobs.

   I have to enforce a default vaule to -maxdepth option since the
   simulation folders contain too many small files.

   optional arguments:

      -p [PATH [PATH ...]], --path [PATH [PATH ...]]
         Searching paths

      -b, --bad

      Print the folders without a valid fb file.

      -u, --unfinished

      Print the unfinished folders.

      -f, --finished

      Print the finished folders.

      -a, --all

      Print all the selected folders; equivalent to "-buf".

      -h, --help

      Show this message and quit

   optional arguments:

      "-maxdepth MAXDEPTH"   maximum search depth, default is 1

      All other long names with single dash will be passed to bash
      find command.

Count_GD.count_GD_finished.process_folders(folders, args)

   Count finished jobs in the current folder.

   Parameters:
      * **folders** (*string list*) -- a list of folders which
        should contain simulations

      * **args** (*name space*) -- command line options

   Returns:
      Print the output on the screen based on args

   Return type:
      No return

Count_GD.count_GD_finished.read_fb_file(fb_fname)

   Return the total number of simulations covered by the folder from a
   fb file.

   The actual simulation is written by Matlab. The first part of the
   simulation code is to provide the total number of simulations the
   code will calculate. The function read the output the retrieve the
   information.

   Parameters:
      **fb_name** (*string*) -- the name of a fb.*txt file

   Returns:
      The number of simulaitons; None if failed

   Return type:
      int

Count_GD.count_GD_finished.read_fb_files()

   Find fb files in current folder and return the total number of
   simulations coverd by the current folder.

   Returns:
      The number of simulaitons coved by the current folder; None if
      failed

   Return type:
      int


Indices and tables
******************

* Index

* Module Index

* Search Page
