#include <stdio.h>
#include <stdlib.h>

int main() {
    int num = 0;
    scanf("%d", &num);

    if (num > 50) {
        if (num <= 100) {
            printf("50 < num <= 100\n");
        } else {
            printf("100 < num\n");
            exit(1);
        }
    } else {
        printf("num <= 50\n");
    }
}
// gcc example.c
