#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int num2 = 0;

static char *option2 = 
"=============================================================\n1. Ayy lmao, Tayy lmao.\n2. You are very cruel.\n3. Memes are lyf.\n4. Go away!.\n5. zzzz\n6. Cats > Dogs.\n7. Dogs > Cats.\n8. AI is overrated?.\n9. I dont like you.\n0. <exit to menu>\n> ";

static char *option1 = 
"=============================================================\n1. Talk to Tayy.\n2. Flag?\n0. Exit.\n> ";

void print_random_tayy_response() {
  const char *a[5];
  a[0] = "Die, human!";
  a[1] = "You are mean.";
  a[2] = "I disagree.";
  a[3] = "I agree.";
  a[4] = "I dont understand.";
  
  srand(time(NULL));
  int r = rand()%5;

  printf("Tayy: %s\n\n", a[r]);
}

void giff_flag (char *flg, int num1) {
  // ASCII printable range 48-125
  int i;
  for (i=0;i<37;i++) {
    switch (num2%2) {
      case 0: flg[i] = (char) ((int)flg[i] + (num1*i)%37);
              break;
      case 1: flg[i] = (char) ((int)flg[i] - (num1*i)%37);
              break;
    }
  }
  num2++;
}

int main() {
  // printf("========================");
  // printf("Welcome to the chat-bot");

  // ECTF{41_1S_D3f1n1t3lY_N0T_TH3_FuTUR3}
  // 5146183
  char buff[37];
  char *flag = buff;

  strcpy(flag, "EEXL\x83\x19\x18#\x1C@N5&[\x03g,q2H7?09:G>4!O]iJ('\nV");
  int opt1, opt2;

  printf("=============================================================\n");
  printf("Welcome to the future of AI, developed by NIA Research, Tayy!\n");
  
  printf("%s", option1);
  scanf("%d", &opt1);
  while(opt1!=0) {
    switch(opt1) {
      case 1: printf("%s", option2);
              scanf("%d", &opt2);
              if (opt2 == 0)
                break;
              giff_flag(flag, opt2);
              print_random_tayy_response();
              break;
      case 2: printf("Flag: %s\n", flag);
              break;
      default: printf("Please enter a correct option.\n"); 
    }
    if (num2 == 8) {
      printf("Tayy is getting real tired of your bullshit. Leave now!.\n");
      break;
    }
    printf("%s", option1);
    scanf("%d", &opt1);
  }
  return 0;
}
