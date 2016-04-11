#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

  /* it's a C program, what can I say? */
  return(0);

}

/* parse all recieved information */
void getAllParams() {

}

/* parse specific key into a variable name for later use */
void getParam(const char *Name, char *Value) {

}
