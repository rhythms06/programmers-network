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
    form = None
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

# counter for line in friendlist, and therefore friends.txt
i = 0

# will hold the current user's line number in friends.txt
n = -1

# find out where in friends.txt are the user's friends, and update variables as such
for (user, friends) in [ ( entry.split(' ', 1) ) for entry in friendlist ]:
    i = i + 1
    if ( user == username ):
        n = i - 1
        oldfriendsline += friends.split()
        oldfriends += friends.split()
        break

# populate friendreqs based on information given from makefriends.py. ignore current user's key.
if form is None:
    error = "Note: cgi.FieldStorage() could not be accessed. You're probably running this through a terminal :)"
elif form:
    error = None
    for key in form.keys():
        if (key != "username"): friendreqs += [key]
else:
    print """
    Something's gone awry.
    Are you in terminal? We don't handle friend requests in terminal.
    You can pass a username as an argument as a test, but if you really
    want to add friends, head to the internets :)
    """

# merge the old friend list with the friend requests. note that this method does not allow a user to undo any friend requests.
newfriends = list(set(oldfriends) | set(friendreqs))

# create the new line to go in friends.txt
newfriendsline += [ username ]
newfriendsline += newfriends

# open up friends.txt...
with open('../friends.txt', 'r') as file:
    # read a list of lines into data
    data = file.readlines()

# update relevant line in friends.txt through data

# add a line in friends.txt if current user doesn't have a line
# else, update the old line
if (n == -1):
	data += ["\n"]
	n = len(data) - 1
else: data[n] = ""

for token in newfriendsline:
    if token is None:
        error = "newfriendsline could not be used. You're probably running this through a terminal :)"
        exit()
    elif token:
        data[n] += token
        # add spaces in between usernames
        if (token != newfriendsline[len(newfriendsline)-1]): data[n] += " "

# ...and write everything back
with open('../friends.txt', 'w') as file:
    file.writelines( data )

# a link to the dashboard. it's standalone because why not
dashboardlink = "\"../../~jinsco/cgi-bin/dashboard.py\""

# HTML and CSS time.
htmlheaders = """

<html>
	<head>
		<title>Confirmation</title>
	</head>

	<style type="text/css">
		html, body {
			margin: 0px;
			height: 100%;
			background-color: #111111;
			color: #dddddd;
		}
		#header {
			position: absolute;
			top: 0%;
			left: 0%;
			height: 10%;
			width: 85%;
			color: #33ccff;
		}
		#main-container {
			position: relative;
			top: 100px;
			left: 80px;
		}
		#pagetitle {
			position: relative;
			top: 20px;
			left: 80px;
			font-size: 40px;
		}
		.line {
			display: block;
			margin-top: 0.5em;
			margin-bottom: 0.5em;
			margin-left: auto;
			margin-right: auto;
			border-style: inset;
			border-width: 1px;
		}
		#topline {
			position: relative;
			margin-top: 1.5em;
			margin-left: 2%;
			margin-right: 2%;
		}
	</style>
	<body>
		<div id="header">
			<div id="pagetitle">Congrats on your new friend list!</div>
			<hr class="line" id="topline"></div>
		</div>
		<div id="main-container">
"""

# oldl = "<p>This is your old line:"
oldf = "<p></p>Your old list of friends:"
reqs = "</p><p>You requested to add the following users to your friends list:"
newf = "</p><p>Your new list of friends:"
# newl = "</p><p>This is your new line:"

button = """</p>
<form action=""" + dashboardlink + """ method="post">
    			<button name="username" value="%s">Go Back to Dashboard</button>
		</form>
""" % username

htmlfooters = """
		</div>
	</body>
</html>
"""

print "Content-Type:text/html;charset=utf-8"
print
print htmlheaders
if error is not None: print error
# print oldl
# print ', '.join(oldfriendsline) + '.'
print oldf
print ', '.join(oldfriends) + '.'
print reqs
print ', '.join(friendreqs) + '.'
print newf
print ', '.join(newfriends) + '.'
print button
# print newl
# print ', '.join(newfriendsline) + '.'
print htmlfooters
