# tsp50ctlserver


#how to use this file, in the master directory

export FLASK_APP=server.py

flask run --host=ip

//functions
default port = 5000

ip:port/getint		#get the int value

ip:port/getbin		#get a binary value

ip:port/post?n=		#post an int value to server

ip:port/allon		#turn on all 7 LED

ip:port/alloff		#turn off all 7 LED

ip:port/reset		#reset tsp50 configuration
