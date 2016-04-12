#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
# Author: Sakib Rasul
# Date: April 2016
# File: makefriends.py
#

# cgi to receive input from previous page
import cgi
# sys to take input from terminal (mainly for testing)
import sys

# Get the username that was submitted via CGI or via command-line
if len(sys.argv) > 1:
	username = sys.argv[1]
else:
	form = cgi.FieldStorage();
	username = form.getvalue("username")

# array of all users and respective full names in database
users = [  ]

# array of all lines in users.txt
userlist = [ line.rstrip('\r\n') for line in open('../../../ascott40/public_html/users.txt') ]

# add (username, full name) to users array for every user
for i in range(0, len(userlist) - 3):
	if ( i % 4 == 0 ):
		users += [ (userlist[i], userlist[i+2]) ]
