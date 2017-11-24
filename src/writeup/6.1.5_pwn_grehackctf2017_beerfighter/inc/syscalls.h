#ifndef __SYSCALLS_H__
#define __SYSCALLS_H__

#include <types.h>

void* syscall0(
                uintptr number
              );

void* syscall3(
                uintptr number,
                void* arg1,
                void* arg2,
                void* arg3
              );

#endif
