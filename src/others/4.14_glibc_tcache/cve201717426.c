#include <stdio.h>
#include <stdlib.h>

int main() {
    void *x = malloc(10);
    printf("malloc(10): %p\n", x);
    free(x);

    void *y = malloc(((size_t)~0) - 2); // overflow allocation (size_t.max-2)
    printf("malloc(((size_t)~0) - 2): %p\n", y);
}
