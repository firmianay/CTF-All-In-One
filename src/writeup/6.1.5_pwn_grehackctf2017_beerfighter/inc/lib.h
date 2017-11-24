#ifndef __LIB__H_
#define __LIB_H__

#include "syscall_constants.h"
#include "strings.h"
#include "io.h"

#define SIZEBUF 2048
#define SIZENAME 1024

struct Character{
        char name[SIZENAME];
        unsigned int level;
};

void city_hall(struct Character* perso);

void welcome_message();

int village_place(struct Character* perso);

void bar();

void champion();

#endif
