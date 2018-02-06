from z3 import *

solver = Solver()

serial = [Int("serial[%d]" % i) for i in range(20)]

solver.add(serial[15] + serial[4]  == 10)
solver.add(serial[1]  * serial[18] == 2 )
solver.add(serial[15] / serial[9]  == 1)
solver.add(serial[17] - serial[0]  == 4)
solver.add(serial[5]  - serial[17] == -1)
solver.add(serial[15] - serial[1]  == 5)
solver.add(serial[1]  * serial[10] == 18)
solver.add(serial[8]  + serial[13] == 14)
solver.add(serial[18] * serial[8]  == 5)
solver.add(serial[4]  * serial[11] == 0)
solver.add(serial[8]  + serial[9]  == 12)
solver.add(serial[12] - serial[19] == 1)
solver.add(serial[9]  % serial[17] == 7)
solver.add(serial[14] * serial[16] == 40)
solver.add(serial[7]  - serial[4]  == 1)
solver.add(serial[6]  + serial[0]  == 6)
solver.add(serial[2]  - serial[16] == 0)
solver.add(serial[4]  - serial[6]  == 1)
solver.add(serial[0]  % serial[5]  == 4)
solver.add(serial[5]  * serial[11] == 0)
solver.add(serial[10] % serial[15] == 2)
solver.add(serial[11] / serial[3]  == 0)    # serial[3] can't be 0
solver.add(serial[14] - serial[13] == -4)
solver.add(serial[18] + serial[19] == 3)

for i in range(20):
    solver.add(serial[i] >= 0, serial[i] < 10)

solver.add(serial[3] != 0)

if solver.check() == sat:
    m = solver.model()
    for d in m.decls():
        print("%s = %s" % (d.name(), m[d]))

    print("".join([str(m.eval(serial[i])) for i in range(20)]))
