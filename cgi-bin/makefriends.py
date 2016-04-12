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

# HTML for checkbox list of users
userlisthtml = ""

# "usernam" is spelled funny to avoid conflict with current username variable
for (usernam, fullname) in users:
	# don't list username if it's the person who's logged in!
	# we have a strict don't-friend-yourself rule around here :P
	if (usernam != username):
		userlisthtml += "\t\t\t<input type=\"checkbox\" name=\"%s\" value=\"ADD\"> %s (%s)<br>\n" % (usernam, fullname, usernam)

# a link to the dashboard. it's standalone because why not
dashboardlink = "\"../../~jinsco/cgi-bin/dashboard.py\""

# HTML and CSS time.
htmlheaders = """

<html>
	<head>
		<title>Make a Friend</title>
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
			<div id="pagetitle">Make a Friend</div>
			<hr class="line" id="topline"></div>
		</div>
		<div id="main-container">
"""

body = """
		<p>
		The following is a list of all the users in our database. Please choose who you'd like to add as friends (if any).
		</p>

		<form action="newfriends.py" method="get">
			<p>
""" + userlisthtml + """			</p>
			<p>
  			<button name="username" value="%s">Submit</button>
			</p>
		</form>
		<form action=""" % username + dashboardlink + """ method="post">
    			<button name="username" value="%s">Go Back to Dashboard</button>
		</form>
""" % username + """
		<p>P.S. You're currently logged in as "%s". If that's not you,
		<a href="http://cs.mcgill.ca/~ascott40">click here</a> to logout.</p>
""" % username

htmlfooters = """
		</div>
	</body>
</html>
"""


# Now send the HTML page to the user's browser
print "Content-Type:text/html;charset=utf-8"
print
if username:
	print htmlheaders
	print body
	print htmlfooters
if username == None:
	print htmlheaders
	print "You're not logged in!"
	print """
	<p>
		<form action="../../~ascott40/login.html">
			<button name="goback">Register/Login</button>
		</form>
	</p>
	"""
	print htmlfooters
