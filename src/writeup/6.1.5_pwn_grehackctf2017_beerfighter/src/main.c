#include "syscalls.h"        
#include "io.h"
#include "lib.h"

char a[6] = {5, 8, 7, 6, 2, 7};

int main(int argc, char **argv){
        struct Character perso = { "Newcomer", 0};

        welcome_message();
        while(village_place(&perso));

        puts("\n");

        return 0;
}
