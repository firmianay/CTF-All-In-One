#include<stdio.h>
#include<string.h>
void main() {
	char pwd[] = "abc123";
	char str[128];
	int flag = 1;
	scanf("%s", str);
	for (int i=0; i<=strlen(pwd); i++) {
    	    if (pwd[i]!=str[i] || str[i]=='\0'&&pwd[i]!='\0' || str[i]!='\0'&&pwd[i]=='\0') {
		flag = 0;
	    }
	}
	if (flag==0) {
	    printf("Bad!\n");
	} else {
	    printf("Good!\n");
	}
}
