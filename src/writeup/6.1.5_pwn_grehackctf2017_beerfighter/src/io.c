#include "io.h"

static intptr write(int fd, void const* data, uintptr nbytes){
        return (intptr) syscall3(
                        SYS_write, /* SYS_write */
                        (void*)(intptr) fd,
                        (void*)data,
                        (void*)nbytes
                        );
}

uintptr strlen(char const* str){
        char const *p;
        for(p=str; *p; p++);
        return p - str;
}

uintptr puts(char const* str){
        return write(STDOUT, str, strlen(str));
}

intptr read(int fd, char* buf, uintptr count){
        return (intptr) syscall3(
                        SYS_read,
                        (void*)(intptr) fd,
                        (void*) buf,
                        (void*) count
                        );
}

int getchar(void){
        char c[1];
        read(STDIN, c, 1);
        return (int) c[0];
}

char* gets(char* str){
        char c;
        char *r = str;
        for(c=getchar(); c != '\n' && c != '\0'; str++, c=getchar()){
                *str = c;
        }
        *str = '\0';
        return r;
}

char* fgets(char *str, int n, int stream){
        char c=getchar();
        int i = 0;
        char *r = str;
        char d[2];
        while(c != '\n'){
                if(i<n-1){
                        *str = c;
                        str++;
                }
                i++;
                c = getchar();
        }
        *str = '\0';
        return r;
}

int getdigit(char *inputphrase, int a, int b){
        char str[3];
        puts(inputphrase);
        fgets(str, 3, STDIN);
        while(strlen(str) != 1 || str[0]>57-9+b || str[0]<48+a){
                puts("Invalid number, try again.\n");
                puts(inputphrase);
                fgets(str, 3, STDIN);
                puts("\n");
        }
        return str[0]-48;
}
