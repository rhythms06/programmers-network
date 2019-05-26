# The Programmer's Network
The Programmer's Network is a very basic social media site made by two classmates and I for a final project in a CS course. It includes:
+ a landing page, which can be found at https://www.cs.mcgill.ca/~ascott40/
+ a sign (in/up) page implemented in HTML (by a teammate) which can be found at https://www.cs.mcgill.ca/~ascott40/login.html
+ a log-in page implemented in C (by a teammate) that validates a user's credentials before taking them to their dashboard
+ a dashboard implemented in Python (by a teammate) in which a user can view text posts penned by them and their friends, pen their own posts, and log out
+ a programatically updated list of users that have friends and the names of their friends (each line is formatted as `username friend1 friend2 ...`), which can be found at https://www.cs.mcgill.ca/~srasul1/friends.txt (a static copy can be viewed in this repo)
+ a "make a friend" page, implemented in Python by me (see cgi-bin/) in which a user can choose to make friends from a list of full and short names of the network's users; upon clicking "Submit," friends.txt is updated accordingly and the user is taken to a confirmation page
+ a "see a friend" page, implemented in C by me (see seefriends.c) in which a user can view the names and submitted details (e.g. professions) of each of their friends
