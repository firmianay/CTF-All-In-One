#!/usr/bin/env python

import angr

main  = 0x004007da
find  = 0x00404fda  # leave;ret
avoid = 0x00400590  # puts@plt

p = angr.Project('./angrybird_org')
init = p.factory.blank_state(addr=main)
pg = p.factory.simgr(init, threads=4)
ex = pg.explore(find=find, avoid=avoid)

final = ex.found[0].state
flag = final.posix.dumps(0)

print "Flag:", final.posix.dumps(1)
