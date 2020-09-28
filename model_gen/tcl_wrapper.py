#!/usr/bin/python3

import os
import sys
import tkinter

tclsh = tkinter.Tcl()
tclsh.eval('set argv0 {{{}}}'.format(sys.argv[1]))
tclsh.eval('set argv {}; set argc 0')

for a in sys.argv[2:]:
    tclsh.eval('lappend argv {{{}}}; incr argc'.format(a))
tclsh.eval('source $argv0')
