#include <stdio.h>
#include <unistd.h>
void main() {
        void *curr_brk, *tmp_brk, *pre_brk;

        printf("当前进程 PID：%d\n", getpid());

        tmp_brk = curr_brk = sbrk(0);
        printf("初始化后的结束地址：%p\n", curr_brk);
        getchar();

        brk(curr_brk+4096);
        curr_brk = sbrk(0);
        printf("brk 之后的结束地址：%p\n", curr_brk);
        getchar();
        
        pre_brk = sbrk(4096);
        curr_brk = sbrk(0);
        printf("sbrk 返回值（即之前的结束地址）：%p\n", pre_brk);
        printf("sbrk 之后的结束地址：%p\n", curr_brk);
        getchar();

        brk(tmp_brk);
        curr_brk = sbrk(0);
        printf("恢复到初始化时的结束地址：%p\n", curr_brk);
        getchar();
}
