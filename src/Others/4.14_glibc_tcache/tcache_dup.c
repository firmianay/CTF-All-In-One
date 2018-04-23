#include <stdlib.h>
#include <stdio.h>

int main() {
    void *p1 = malloc(0x10);
    printf("1st malloc(0x10): %p\n", p1);
    printf("Freeing the first one\n");
    free(p1);
    printf("Freeing the first one again\n");
    free(p1);
    printf("2nd malloc(0x10): %p\n", malloc(0x10));
    printf("3rd malloc(0x10): %p\n", malloc(0x10));
}
