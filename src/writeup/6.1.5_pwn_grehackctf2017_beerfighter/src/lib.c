#include "lib.h"


void welcome_message(){
        char *message = "\n"
                "__________________________________\n"
                "\n"
                "--- Welcome in  BeerFigher III ---\n"
                "__________________________________\n"
                "\n"
                "You just arrived in the small village of Foo in\n"
                "the country, after a long day of travel.\n"
                "Thirsty, you could just go and grab a beer at the\n"
                "bar. You may also go in the city hall and get\n"
                "registered with the mayor.\n"
                "\n"
                "\n";
        puts(message);
}

void city_hall(struct Character* perso){
        char digit;
        char name[SIZEBUF];
        puts("Welcome ");
        puts(perso->name);
        puts("! I am the mayor of this small town and my role is to register the names of its citizens.\nHow should I call you?\n");
        puts("[0] Tell him your name\n");
        puts("[1] Leave\n");
        digit = getdigit("Type your action number > ", 0, 1);

        switch(digit){
        case 0:
                puts("Type your character name here > ");
                fgets(name, SIZEBUF, STDIN);
                strncpy(perso->name, name, SIZEBUF);
                puts("\n");
                break;
        case 1:
                puts("You just left the old man without even saying \"Good bye\"\n");
                break;
        default:
                puts("Invalid action\n");
                break;
        }
}

int village_place(struct Character* perso){
        char *message = "\n\n"
		"   ~         ~~          __\n"
		"        _T      .,,.    ~--~ ^^\n"
		"  ^^   // \\                    ~\n"
		"       ][O]    ^^      ,-~ ~\n"
		"    /''-I_I         _II____\n"
		" __/_  /   \\ ______/ ''   /'\\_,__\n"
		"   | II--'''' \\,--:--..,_/,.-{ },\n"
		" ; '/__\\,.--';|   |[] .-.| O{ _ }\n"
		" :' |  | []  -|   ''--:.;[,.'\\,/\n"
		" '  |[]|,.--'' '',   ''-,.    |\n"
		"   ..    ..-''    ;       ''. '\n"
                "\n"
                "You are in the village square.\n"
                "In front of you can see the entrance of the local\n"
                "bar from where one could hear laughter and singing.\n"
                "On your\n"
                "left stands is the massive front of the city hall that\n"
                "dominates the village. On your right, in the \n"
                "shadow of the bar, an alley filled with unconscious bodies and\n"
                "empty pints leads to a dark yard where the most\n"
                "valiant barflies of the country can face each other.\n"
                "It's time to choose in which place you will enter !\n"
                "------------\n\n";
        char *choice0 = "[0] The bar\n";
        char *choice1 = "[1] The City Hall\n";
        char *choice2 = "[2] The dark yard\n";
        char *choice3 = "[3] Leave the town for ever\n";

        puts(message);
        puts(choice0);
        puts(choice1);
        puts(choice2);
        puts(choice3);
        int digit = getdigit("Type your action number > ", 0, 3);

        switch(digit){
        case 0:
                bar();
                break;
        case 1:
                city_hall(perso);
                break;
        case 2:
                champion();
                break;
        case 3:
                puts("By !\n");
                return 0;
                break;
        default:
                puts("Invalid choice\n");
                break;
        }
        return 1;
}

void bar(){
        char digit;
        char *message = "\n\n" 
                "   _.._..,_,_ \n"
		"  (          )\n"
		"   ]~,\"-.-~~[	  Welcome in Foo bar\n"
		" .=])' (;  ([            ---\n"
		" | ]:: '    [   We are currently close\n"
		" '=]): .)  ([   Please, come back later\n"
		"   |:: '    |\n"
		"    ~~----~~\n"
                "\n\n";
        puts(message);

        puts("[0] Leave\n");
        digit = getdigit("Type your action number > ", 0, 0);
        switch(digit){
        case 0:
                puts("You just left the bar\n");
                break;
        default:
                puts("Invalid action\n");
                break;
        }
}

void champion(){
        char digit;
        puts("\n\n-- Feature currently in development...\n\n");
        puts("[0] Leave\n");
        digit = getdigit("Type your action number > ", 0, 0);
        switch(digit){
        case 0:
                puts("You just left the yard\n");
                break;
        default:
                puts("Invalid action\n");
                break;
        }
}
