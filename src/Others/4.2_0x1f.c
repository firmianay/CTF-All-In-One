#include<stdio.h>
#include<string.h>
void main() {
    char data[8];
    char str[8];
    printf("请输入十六进制为 0x1f 的字符: ");
    sprintf(str, "%c", 31);
    scanf("%s", data);
    if (!strcmp((const char *)data, (const char *)str)) {
        printf("correct\n");
    } else {
        printf("wrong\n");
    }
}
