#include<stdio.h>
void main() {
    char format[128];
    int arg1 = 1, arg2 = 0x88888888, arg3 = -1;
    char arg4[10] = "ABCD";
    scanf("%s", format);
    printf(format, arg1, arg2, arg3, arg4);
    printf("\n");
}
