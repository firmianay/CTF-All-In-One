#include <stdlib.h>
#include <stdio.h>
#include <mcheck.h>

void main() {
    char *p;
    
    mtrace();

    calloc(16, 16);
    fprintf(stderr, "calloc some chunks that will not be freed\n");

    p = malloc(1000);
    fprintf(stderr, "About to free\n");
    free(p);
    fprintf(stderr, "About to free a second time\n");
    free(p);
    fprintf(stderr, "Finish\n");

    muntrace();
}
