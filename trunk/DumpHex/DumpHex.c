/* --- The following code comes from d:\program files\lcc\lib\wizard\textmode.tpl. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*------------ global parameters -----------*/
char *version = "0.1";
char *last_update = "2006.07.06";

/*------------------------------------------*/


void Usage(char *programName)
{
	fprintf(stderr,"Dump the beginning 10 Bytes of the file specific.\n" );
	fprintf(stderr,"written by Ö£ÐÂÐÇ <zhengxinxing@gmail.com>, %s\n", last_update );
	fprintf(stderr,"Version: %s\n", version);
	fprintf(stderr,"usage: %s <file>\n" , programName);
	/* Modify here to add your usage message when the program is
	 * called without arguments */
}

/* returns the index of the first argument that is not an option; i.e.
   does not start with a dash or a slash
*/
int HandleOptions(int argc,char *argv[])
{
	int i,firstnonoption=0;

	for (i=1; i< argc;i++) {
		if (argv[i][0] == '/' || argv[i][0] == '-') {
			switch (argv[i][1]) {
				/* An argument -? means help is requested */
				case '?':
					Usage(argv[0]);
					break;
				case 'h':
				case 'H':
					if (!stricmp(argv[i]+1,"help")) {
						Usage(argv[0]);
						break;
					}
					/* If the option -h means anything else
					 * in your application add code here
					 * Note: this falls through to the default
					 * to print an "unknow option" message
					*/
				/* add your option switches here */

				default:
					fprintf(stderr,"unknown option %s\n",argv[i]);
					break;
			}
		}
		else {
			firstnonoption = i;
			break;
		}
	}
	return firstnonoption;
}

void printHexFromFile(FILE * file)
{
	char c;
	int count = 0;

	/*c = fgetc(file);
	while (c != EOF){
		printf("%02x ", (unsigned char)c);
		c = fgetc(file);
		count ++;
	}*/
	for(int i=0; i<10; i++){
		c = fgetc(file);
		printf("%02x ", (unsigned char)c);
		//count++;
	}
	printf("\n");

	return;
}



int main(int argc,char *argv[])
{
	if (argc == 1 || argc >=3) {
		/* If no arguments we call the Usage routine and exit */
		Usage(argv[0]);
		return 1;
	}
	/* handle the program options */
	if (HandleOptions(argc,argv) == 0){
	    return 0;
	}
	
	/* The code of your application goes here */
	char * file = argv[1];

	FILE * targetFile = fopen(file, "rb");
	if(targetFile == NULL){
		printf("cannot open %s", file);
		return 1;
	}


	printf("dump %s as hex:\n", file);
	printf("*****************************\n");
	printHexFromFile(targetFile);
	printf("*****************************");

	return 0;
}

