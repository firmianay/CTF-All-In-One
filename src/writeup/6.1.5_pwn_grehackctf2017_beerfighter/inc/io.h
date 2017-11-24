#ifndef __IO_H__
#define __IO_H__

#include "types.h"
#include "syscall_constants.h"
#include "syscalls.h"

#define STDIN 0
#define STDOUT 1
#define STDERR 2

static intptr write(int fd, void const* data, uintptr nbytes);

uintptr strlen(char const* str);

uintptr puts(char const* str);

intptr read(int fd, char* buf, uintptr count);

int getchar(void);

char* gets(char* str);

char* fgets(char *str, int n, int stream);

int getdigit(char *inputphrase, int a, int b);

#endif
