#include <errno.h>
#include <stdio.h>
#include <pthread.h>
#include <asm/prctl.h>
#include <sys/prctl.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

size_t get_long() {
    char buf[8];
    fgets(buf, 8, stdin);
    return (size_t)atol(buf);
}
size_t readn(int fd, char *buf, size_t n) {
	size_t rc;
	size_t nread = 0;
	while (nread < n) {
		rc = read(fd, &buf[nread], n-nread);
		if (rc == -1) {
			if (errno == EAGAIN || errno == EINTR) {
				continue;
			}
			return -1;
		}
		if (rc == 0) {
			break;
		}
		nread += rc;

	}
	return nread;
}
void * start() {
    size_t size;
    char input[0x1000];
    memset(input, 0, 0x1000);
    puts("Welcome to babystack 2018!");
    puts("How many bytes do you want to send?");
    size = get_long();
    if (size > 0x10000) {
        puts("You are greedy!");
        return 0;
    }
    readn(0, input, size);
    puts("It's time to say goodbye.");
    return 0;
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    pthread_t t;
    puts("");
    puts(" #   #    ####    #####  ######");
    puts("  # #    #    #     #    #");
    puts("### ###  #          #    #####");
    puts("  # #    #          #    #");
    puts(" #   #   #    #     #    #");
    puts("          ####      #    #");
    puts("");
    pthread_create(&t, NULL, &start, 0);
    if (pthread_join(t, NULL) != 0) {
        puts("exit failure");
        return 1;
    }
    puts("Bye bye");
    return 0;
}

