#!/usr/bin/python3

import tkinter
import sys
import os

# _curr_dir = os.path.dirname(os.path.realpath(__file__))

tclsh = tkinter.Tcl()
script_name = sys.argv[1] # os.path.join(_curr_dir, "model_gen.tcl")
tclsh.eval('set argv0 {{{}}}'.format(script_name))
tclsh.eval('set argv {}; set argc 0')

for a in sys.argv[2:]:
    tclsh.eval('lappend argv {{{}}}; incr argc'.format(a))
tclsh.eval('source $argv0')

