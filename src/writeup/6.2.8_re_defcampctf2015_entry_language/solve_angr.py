#!/usr/bin/env python

import angr

project = angr.Project("entry_language", auto_load_libs=False)

@project.hook(0x400844)
def print_flag(state):
    print "FLAG SHOULD BE:", state.posix.dump_fd(0)
    project.terminate_execution()

project.execute()
