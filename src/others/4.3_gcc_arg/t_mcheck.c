#include <stdlib.h>
#include <stdio.h>

void main() {
    char *p;
    p = malloc(1000);
    fprintf(stderr, "About to free\n");
    free(p);
    fprintf(stderr, "About to free a second time\n");
    free(p);
    fprintf(stderr, "Finish\n");
}
