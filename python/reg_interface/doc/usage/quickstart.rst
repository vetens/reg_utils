Quickstart guide
================
This guide describes in short how to run the reg_interface tool on the host PC. 

After the installation the executable scripts has to be added to the system $PATH variable. Following this one can start the Command Line Interface by simply running

>>> reg.py

In the appeared command prompt type:

>>> connect eagleXX

where eagleXX is the name of the board you want to use (eagle33 @P5, eagle34 @904 Integration Stand, eagle26 @QC8).

A command prompt will appear, allowing you to perform single or multi register write/read operations. Examples:

>>> read reg_name 

will return the register value.

>>> write reg_name value 

will write the value to the register.

CLI support tab completion for these operations.

>>> fw 

will return firmware version information for all links.

>>> kw pattern

will return read of all the registers containing "pattern" is their names. 

>>> outputnode reg_name 

will output node's address, mask, permissions and eventual comments describing what it controls and which values can take

>>> broadcastOH mask action reg_name opt_value 

will broadcast read or write reg_name command to all optohybrids specified in the mask. reg_name should start from the part after OHX in full register name. 

Example: 

>>> broadcastOH 0-3,5 read STATUS.FW.DATE

expected output should look like this (in this system only link 0 has OH connected):

     >>> 0x65030000 r    GEM_AMC.OH.OH0.STATUS.FW.DATE                           0x20170505
     >>> 0x65070000 r    GEM_AMC.OH.OH1.STATUS.FW.DATE                           Bus Error
     >>> 0x650b0000 r    GEM_AMC.OH.OH2.STATUS.FW.DATE                           Bus Error
     >>> 0x650f0000 r    GEM_AMC.OH.OH3.STATUS.FW.DATE                           Bus Error
     >>> 0x65170000 r    GEM_AMC.OH.OH5.STATUS.FW.DATE                           Bus Error
