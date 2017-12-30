#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>
void main() {
        void *curr_brk;
		
        printf("当前进程 PID：%d\n", getpid());
        printf("初始化后\n");
        getchar();
        
        char *addr;
        addr = mmap(NULL, (size_t)4096, PROT_READ|PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
        printf("mmap 完成\n");
        getchar();

        munmap(addr, (size_t)4096);
        printf("munmap 完成\n");
        getchar();
}
