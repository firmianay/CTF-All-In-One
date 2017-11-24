#include "strings.h"

char* strncpy(char* dest, const char* src, int n){
        char* r = dest;
        for(int i=0; i<n; i++, src++, dest++)
                *dest = *src;
        *dest = 0;

        return r;
}
