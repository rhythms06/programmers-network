#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
# Author: Sakib Rasul
# Date: April 2016
# File: newfriends.py
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

# array of all lines in friends.txt
friendlist = [ line.rstrip('\r\n') for line in open('../friends.txt') ]

# the current user's line in friends.txt before friend requests
oldfriendsline = [  ]
oldfriendsline += [ username ]

# the current user's friend list before friend requests
oldfriends = [  ]

# the user's friend requests
friendreqs = [  ]

# the current user's friend list after friend requests
newfriends = [  ]

# the current user's line in friends.txt after friend requests
newfriendsline = [  ]
