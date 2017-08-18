#include<stdio.h>
#include<string.h>
void validate_passwd(char *passwd) {
	char passwd_buf[11];
	unsigned char passwd_len = strlen(passwd);
	if(passwd_len >= 4 && passwd_len <= 8) {
		printf("good!\n");
		strcpy(passwd_buf, passwd);
	} else {
		printf("bad!\n");
	}
}

int main(int argc, char *argv[]) {
	if(argc != 2) {
		printf("error\n");
		return 0;
	}
	validate_passwd(argv[1]);
}
