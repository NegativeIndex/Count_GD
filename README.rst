Count_GD
===================

Description
===========

GD-Calc is a Matlab based electromagnetic simulation package
implemented RCWA algorithm. The folder tree of a project is shown below.

::

    project
    ├── A1
    │   ├── run.m
    │   ├── fb.txt
    │   └── RawData
    │       └── *.txt
    ├── A2
    │   ├── run.m
    │   ├── fb.txt
    │   └── RawData
    │       └── *.txt

I have to investigate a large parameter space. I divide the project
into several folders (A1, A2, etc.). Each folder covers a portion of
the parameter space and they are independent from each other. So I can
run these folders in parallel. 

Inside one folder, *run.m* is the matlab script, which runs
simulations in series. At the beginning, the script will calculate the
number of simulations covered in this folder and save the information
in the feedback files (*fb.txt*). Each simulation will generate three
text files (reflection, transmission and absorption) saved in the
*RawData* folder. 

The difficulties in this program is that there are many small files in
*RawData* folders. So it will be very slow to use a simple *find*
command. I have to enforce the ``-maxdepth`` option. The *find*
command has the long option name with single dash. This is different
from the argparse module setting. Most part of the program is to try
to transfer the abnormal options to find command.

Examples 
********************

.. code-block:: bash
   
  count_GD_finished.py -name "A*" -u

Running the command at *project* folder will demonstrate the folders
with unfinished simulaitons.

.. code-block:: bash
   
  count_GD_finished.py -p A1 -a

Running the command at *project* folder will demonstrate the
information about the *A1* folder.

 

Argparse_Addon module
=====================

Some improvements over the argparse module. I want long option names
with a single dash.


``Count_GD.Argparse_Addon.long_option_dash_1to2(args)``
   Change the single-dash in front of a long option back to double-
   dash.

``Count_GD.Argparse_Addon.long_option_dash_2to1(args)``
   Change the double-dash in front of a long option to single-dash.

``Count_GD.Argparse_Addon.main(argv)``
   The main function to demonstrate the function of Argparse_Addon
   module. The function try to find some files and process them. The
   unknown options are passed to Linux bash find function.

   I want to enforce a default value to -maxdepth option. I have to
   intercept the parser's help message.

   Usage: 
     ``Argparse_Addon.py [-p [PATH [PATH ...]]] [-s] [-maxdepth MAXDEPTH] [-h]``

   optional arguments:
      ``-p [PATH [PATH ...]], --path [PATH [PATH ...]]``
         Searching paths

      ``-s, --summary`` : Demonstrate only summary

      ``-h, --help`` : Show this message and quit

   option modification:
      ``-maxdepth MAXDEPTH`` : maximum search depth, default is 1

      All other long names with single dash will be passed to bash
      find command.

``Count_GD.Argparse_Addon.modify_help_string(help_string, longnames=None, sentences=None)``
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

Count the number of GD-Calc simulations finished in selected folders.

``Count_GD.count_GD_finished.check_RawData()``
   Count finished jobs in the current folder.

   Returns:
      The number of finished simulations; 0 if failed

   Return type:
      int

``Count_GD.count_GD_finished.main(argv)``
   The main function to find the simulation folders and count the
   finished jobs.

   I have to enforce a default value to -maxdepth option since the
   simulation folders contain too many small files.

   optional arguments:
      ``-p [PATH [PATH ...]], --path [PATH [PATH ...]]`` :     Searching paths

      ``-b, --bad`` :    Print the folders without a valid fb file.

      ``-u, --unfinished`` :   Print the unfinished folders.

      ``-f, --finished`` :    Print the finished folders.

      ``-a, --all`` :         Print all the selected folders; equivalent to "-b -u -f".

      ``-h, --help`` :       Show this message and quit

   optional arguments:
      ``-maxdepth MAXDEPTH`` :   maximum search depth, default is 1

      All other long names with single dash will be passed to bash
      find command.

``Count_GD.count_GD_finished.process_folders(folders, args)``
   Count finished jobs in the current folder.

   Parameters:
      * **folders** (*string list*) -- a list of folders which
        should contain simulations

      * **args** (*name space*) -- command line options

   Returns:
      Print the output on the screen based on args

   Return type:
      No return

``Count_GD.count_GD_finished.read_fb_file(fb_fname)``
   Return the total number of simulations covered by the folder from a
   fb file.

   The actual simulation is written by Matlab. The first part of the
   simulation code is to provide the total number of simulations the
   code will calculate. The function read the output the retrieve the
   information.

   Parameters:
      **fb_name** (*string*) -- the name of a fb.*txt file

   Returns:
      The number of simulations; None if failed

   Return type:
      int

``Count_GD.count_GD_finished.read_fb_files()``
   Find fb files in current folder and return the total number of
   simulations covered by the current folder.

   Returns:
      The number of simulations covered by the current folder; None if
      failed

   Return type:
      int



.. LocalWords: RawData  Calc fb txt args argv argparse maxdepth longnames py 


