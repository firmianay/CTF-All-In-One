#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

#define MAX 0x10

char *users[MAX];
long counts[MAX];
int vote_num;

void read_until_nl_or_max(char *dst, size_t len) {
	size_t i = 0;
	for (;;) {
		if (read(0, &dst[i], 1) == -1)
			exit(1);
		if (dst[i] == '\n') {
			dst[i] = '\0';
			return;
		}
		i++;
		if (i >= len) {
			dst[i - 1] = '\0';
			return;
		}
	}
}

void puts_heapless(char *str) {
    write(1, str, strlen(str));
    write(1, "\n", 1);
    fflush(stdout);
}

void print(char *str) {
	write(1, str, strlen(str));
	fflush(stdout);
}

int read_int() {
	char tmp[8];
	memset(tmp, 0, 8);
	read_until_nl_or_max(tmp, 8);
	return atoi(tmp);
}

void *vote_thread(void *arg) {	
	sleep(3);
	++(counts[vote_num]);
	return NULL;
}

void create() {
	int size;
	char *user;
	int i;
	for (i = 0; i < MAX; i++) {
		if (users[i] == NULL) {
			print("Please enter the name's size: ");
			size = read_int();
			if (size > 0 && size <= 0x1000) {
				user = (char *)malloc(size + 0x10);
				*(long *)(user) = 0;
				*(long *)(&user[8]) = time(NULL);
				print("Please enter the name: ");
				read_until_nl_or_max(&user[16], size);
				users[i] = user;
			}
			return;
		}
	}
}

void show() {
	int index;
	char tmp[266];
	memset(tmp, 0, 266);
	print("Please enter the index: ");
	index = read_int();
	if (index >= 0 && index < MAX && users[index] != NULL) {
		snprintf(tmp, 256, "name: %s\ncount: %lu\ntime: %lu", &users[index][16], *(long *)(users[index]), *(long *)(&users[index][8]));
		puts_heapless(tmp);
	}
}

void vote() {
	int index;
	pthread_t id;
	print("Please enter the index: ");
	index = read_int();
	if (index >= 0 && index < MAX && users[index] != NULL) {
		++(*(long *)(users[index]));
		*(long *)(&users[index][8]) = time(NULL);
		vote_num = index;
		pthread_create(&id, NULL, &vote_thread, NULL);
	}
}

void result() {
	int i;
	char tmp[266];
	memset(tmp, 0, 266);
	for (i = 0; i < MAX; i++) {
		if (counts[i] != 0) {
			snprintf(tmp, 256, "%d\t->\t%lu", i, counts[i]);
			puts_heapless(tmp);
			fflush(stdout);
		}
	}
}

void cancel() {
	int index;
	print("Please enter the index: ");
	index = read_int();
	if (index >= 0 && index < MAX && users[index] != NULL) {
		--(counts[index]);
		--(*(long *)(users[index]));
		if (counts[index] == *(long *)(users[index])) {
			if (counts[index] < 0) {
				free(users[index]);
			}
			return;
		}
		if (counts[index] < 0) {
			printf("%s", &users[vote_num][16]);
			fflush(stdout);
			puts_heapless(" has freed");
			free(users[index]);
			users[index] = 0;
		}
	}	
}

int main(void) {
	setvbuf(stdin, NULL, _IONBF, 0);
	int c;
	alarm(30);
	for (;;) {
		puts_heapless("0: Create");
		puts_heapless("1: Show");
		puts_heapless("2: Vote");
		puts_heapless("3: Result");
		puts_heapless("4: Cancel");
		puts_heapless("5: Exit");
		print("Action: ");
		if (scanf("%d", &c) == EOF)
			exit(1);
		if (c == 0) {
			create();
		}
		if (c == 1) {
			show();
		}
		if (c == 2) {
			vote();
		}
		if (c == 3) {
			result();
		}
		if (c == 4) {
			cancel();
		}
		if (c == 5) {
			puts_heapless("Bye");
			exit(0);
		}
	}
	return 0;
}