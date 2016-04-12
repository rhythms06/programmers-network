#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Helper macro to convert two-character hex strings to character value
#define ToHex(Y) (Y>='0'&&Y<='9'?Y-'0':Y-'A'+10)

// will capture information recieved from dashboard.py
char InputData[4096];

int main(void)
{

  // find out who the current user is
  char username[100] = "";
	getAllParams();
	getParam("username", username);

  /* this username variable is for testing purposes
  const char* testname = "brady";
  */

  /* A bunch of printf's to print out html headers and css */
  printf("Content-Type:text/html\r\n\r\n<html>\n<head>\n<title>See Friends</title>\n</head>\n");

  printf("<style type=\"text/css\">\nhtml, body {\nmargin: 0px;\nheight: 100%;\nbackground-color: #111111;\ncolor: #dddddd;\n}\n");

  printf("#header {\nposition: absolute;\ntop: 20px;\nleft: 5.6%;\nheight: 10%;\nwidth: 85%;\ncolor: #33ccff;\nfont-size: 40px;\n}\n");

  printf("#main-container {\nposition: relative;\ntop: 100px;\nleft: 80px;\n};\n");

  printf(".line {\ndisplay: block;\nmargin-top: 0.5em;\nmargin-bottom: 0.5em;\nmargin-left: auto;\nmargin-right: auto;\nborder-style: inset;\nborder-width: 1px;\n}\n");

  printf("#topline {\nposition: relative;\nmargin-top: 0.1em;\nmargin-left: -4.6%;\nmargin-right: 8.5%;\n}\n");

  printf(".profiles { display: none; }\n");

  printf("</style>\n");

  printf("<body>\n");

  printf("<div id=\"header\">\n");
  // pagetitle refuses to work :(
  // printf("<div id=\"pagetitle\">\n");
  printf("See a Friend");
  // pagetitle div closer tag
  // printf("</div>\n");
  printf("<hr class=\"line\" id=\"topline\"></div>\n");
  printf("</div>\n");
  printf("<div id=\"main-container\">\n");

  //strlen for website usage, ! operand for terminal usage
  if(!username || strlen(username) == 0) {

    // username not usable. get outta here!
    printf("You're not logged in!\n");
    printf("<p><form action=\"../../~ascott40/cgi-bin/login.html\">\n");
    printf("<button name=\"goback\">Register/Login</button>");
    printf("</form></p>");
    printf("</div>\n</body>\n</html>\n");

  // else case for when there is a usable string in variable "username"
  } else {
    printf("<p>Your username is %s. The following is a list of your friends (if any) - click a username to expand a friend's profile!</p>\n", username);

    // read friends.txt, parse each line, and use the line of the current user to populate the webpage.
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("../friends.txt", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    while ((read = getline(&line, &len, fp)) != -1) {
        char ** parsearray = NULL;
        char * p = strtok (line, " ");
        int n_spaces = 0, i;

        /* split line and append its tokens to 'parsearray' */
        while (p) {
          parsearray = realloc (parsearray, sizeof (char*) * ++n_spaces);

          if (parsearray == NULL)
            exit (-1); /* exit if memory allocation failed */

          parsearray[n_spaces-1] = p;

          p = strtok (NULL, " ");
        }

        /* use tokens (friends) if first token (username) matches current user */
        if ((strcmp(parsearray[0], username)) == 0) {
          for (i = 1; i < (n_spaces); ++i) {

            char *fullname;
            char *profession;

            int lines_allocated = 128;
            int max_line_len = 100;

            /* Allocate lines of text to parse users.txt into a array of char arrays 'words' */
            char **words = (char **)malloc(sizeof(char*)*lines_allocated);
            if (words==NULL)
            {
              fprintf(stderr,"Out of memory (1).\n");
              exit(1);
            }

            FILE *fp = fopen("../../../ascott40/public_html/users.txt", "r");
            if (fp == NULL)
            {
              fprintf(stderr,"Error opening file.\n");
              exit(2);
            }

            /* max index of words is words[l] */
            int l;
            for (l=0;1;l++)
            {
              int j;

              /* Have we gone over our line allocation? */
              if (l >= lines_allocated)
              {
                int new_size;

                /* Double our allocation and re-allocate */
                new_size = lines_allocated*2;
                words = (char **)realloc(words,sizeof(char*)*new_size);
                if (words==NULL)
                {
                  fprintf(stderr,"Out of memory.\n");
                  exit(3);
                }
                lines_allocated = new_size;
              }
              /* Allocate space for the next line */
              words[l] = malloc(max_line_len);
              if (words[l]==NULL)
              {
                fprintf(stderr,"Out of memory (3).\n");
                exit(4);
              }
              if (fgets(words[l],max_line_len-1,fp)==NULL)
              break;

              /* Get rid of return or newline at end of line */
              for (j=strlen(words[l])-1;j>=0 && (words[l][j]=='\n' || words[l][j]=='\r');j--)
              ;
              words[l][j+1]='\0';
            }
            /* Close users.txt. 'words' now contains all user info */
            fclose(fp);

            int j;

            /* gather user info for profile iteration */
            for(j = 0; j < l; j++) {
              if ((strcmp(parsearray[i], words[j])) == 0) {
                  fullname = words[j+2];
                  profession = words[j+3];
              }
            }

            /* a fix for the last iteration */
            if (i == (n_spaces)-2) {
              parsearray[i+1][strlen(parsearray[i+1])-1] = '\0';
            }

            /* we're done populating user profiles, so let's free up memory */
            for (;l>=0;l--)
            free(words[l]);
            free(words);

          }

        }

        /* free memory before parsing next line of friends.txt */
        free (parsearray);
    }

    /* close friends.txt, we're done with it */
    fclose(fp);

    /* free line memory */
    if (line) {
      free(line);
    }
  }

  /* it's a C program, what can I say? */
  return(0);

}

/* parse all recieved information */
void getAllParams() {
  // Determines if it is a POST or GET method
	if( getenv( "REQUEST_METHOD" ) == 0 ) {
		printf("No REQUEST_METHOD, must be running in DOS mode\n");
		return;
	} else if (strcmp( getenv("REQUEST_METHOD"), "POST") == 0) {
		// If POST
		char *endptr;	// quite useless, but required
		char *len1 = getenv("CONTENT_LENGTH");
		int contentlength = strtol(len1, &endptr, 10);
		fread(InputData , contentlength, 1, stdin);
	} else {
		// If GET
		strcpy(InputData, getenv("QUERY_STRING"));
	}
}

/* parse specific key into a variable name for later use */
void getParam(const char *Name, char *Value) {
  char *pos1 = strstr(InputData, Name);

	if (pos1) {
		pos1 += strlen(Name);

		if (*pos1 == '=') { // Make sure there is an '=' where we expect it
			pos1++;

			while (*pos1 && *pos1 != '&') { // '&' signifies end of this parameter and the beginning of another

				if (*pos1 == '%') {

					// Convert it to a single ASCII character and store
					*Value++ = (char)ToHex(pos1[1]) * 16 + ToHex(pos1[2]);
					pos1 += 3;

				} else if( *pos1=='+' ) {

					// If it's a '+', store a space
					*Value++ = ' ';
					pos1++;

				} else {

					*Value++ = *pos1++; // Otherwise, just store the character
				}

			}

			*Value++ = '\0';
			return;
		}
	}

	strcpy(Value, "undefined");	// If parameter not found, then use default parameter. Great for debugging.
	return;

}
