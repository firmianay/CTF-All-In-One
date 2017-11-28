#!/usr/bin/env python
# Looks like the serial number verification for space ships is similar to that
# of your robot. Try to find a serial that verifies for this space ship

import sys
print ("Please enter a valid serial number from your RoboCorpIntergalactic purchase")
if len(sys.argv) < 2:
  print ("Usage: %s [serial number]"%sys.argv[0])
  exit()
  
print ("#>" + sys.argv[1] + "<#")

def check_serial(serial):
  if (not set(serial).issubset(set(map(str,range(10))))):
    print ("only numbers allowed")
    return False
  if len(serial) != 20:
    return False
  if int(serial[15]) + int(serial[4]) != 10:
    return False
  if int(serial[1]) * int(serial[18]) != 2:
    return False
  if int(serial[15]) / int(serial[9]) != 1:
    return False
  if int(serial[17]) - int(serial[0]) != 4:
    return False
  if int(serial[5]) - int(serial[17]) != -1:
    return False
  if int(serial[15]) - int(serial[1]) != 5:
    return False
  if int(serial[1]) * int(serial[10]) != 18:
    return False
  if int(serial[8]) + int(serial[13]) != 14:
    return False
  if int(serial[18]) * int(serial[8]) != 5:
    return False
  if int(serial[4]) * int(serial[11]) != 0:
    return False
  if int(serial[8]) + int(serial[9]) != 12:
    return False
  if int(serial[12]) - int(serial[19]) != 1:
    return False
  if int(serial[9]) % int(serial[17]) != 7:
    return False
  if int(serial[14]) * int(serial[16]) != 40:
    return False
  if int(serial[7]) - int(serial[4]) != 1:
    return False
  if int(serial[6]) + int(serial[0]) != 6:
    return False
  if int(serial[2]) - int(serial[16]) != 0:
    return False
  if int(serial[4]) - int(serial[6]) != 1:
    return False
  if int(serial[0]) % int(serial[5]) != 4:
    return False
  if int(serial[5]) * int(serial[11]) != 0:
    return False
  if int(serial[10]) % int(serial[15]) != 2:
    return False
  if int(serial[11]) / int(serial[3]) != 0:
    return False
  if int(serial[14]) - int(serial[13]) != -4:
    return False
  if int(serial[18]) + int(serial[19]) != 3:
    return False
  return True

if check_serial(sys.argv[1]):
  print ("Thank you! Your product has been verified!")
else:
  print ("I'm sorry that is incorrect. Please use a valid RoboCorpIntergalactic serial number")
