Count_GD
===================

Description
===========
A simple Python code to count the finished GD-Calc simulaitons.

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
command. I have to enforce the ``-maxdepth`` option. We can also use
all the options supported by find command here since all the unknown
options will be passed find command.

Examples 
********************

.. code-block:: bash
   
  count_GD_finished.py -name "A*" -u

Running the command at *project* folder will demonstrate the folders
with unfinished simulations.

.. code-block:: bash
   
  count_GD_finished.py -p A1 -a

Running the command at *project* folder will demonstrate the
information about the *A1* folder.

count_GD_finished module
========================

Count the number of GD-Calc simulations finished in selected folders.

``Count_GD.count_GD_finished.append_help_string(help_string, sentences=None)``
   Append sentences at the end of the help_string. 

   Parameters:
      * **help_string** (*string*) -- the string return by
        parser.format_help()

      * **sentences** (*string list*) -- The sentences added at the
        end

   Returns:
      The new version of help string

   Return type:
      string


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

      ``-a, --all`` :         Print all the selected folders; equivalent to "-buf".

      ``-h, --help`` :       Show this message and quit

      ``-maxdepth MAXDEPTH`` :   maximum search depth, default is 1

      All the other unknown options will be passed to bash
      find command to find the corresponding folders.

``Count_GD.count_GD_finished.process_folders(folders, args)`` 
   Count finished jobs in many folders. Print the results based on
   commnad line options.

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


