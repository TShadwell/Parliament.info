#!c:\Python32\python.exe
import cgi
from math import floor
from mpfuncs import mpinfo
from urllib.request import urlopen, unquote, quote
from urllib.error import HTTPError
from string import punctuation
from sys import path
from json import loads
print ("Content-Type: text/html")
print ()

form = cgi.FieldStorage()
out = ""



if "q" in form:
	
	q  = form["q"].value.lower()

	#Start trying to work out what they want.
	#See if they want to know _who_ their mp is.
	if  ( (not q.find("mp") == -1) and ( not q.find("for") == -1)):
		#Open connection, strip punctuation and locate postcode
		con = urlopen("http://www.theyworkforyou.com/api/getMP?postcode=" + ''.join(''.join(ch for ch in q if ch not in set(punctuation)).split("for")[-1].split(' ')) + "&output=json&key=DiEfMMDNP6g6EGaNC4AN4Lwb")
		#Parse JSON
		data = loads(con.read().decode())

		#Be kind to servers
		con.close()
		#Get more information
		out = mpinfo(data)

	elif  ( ( (not q.find("mp") == -1) and (not q.find("who") == -1 ) )  and (q.find("for") ==-1)):
		out ="If you're looking for your MP, ask: <i>Who is the mp for <b class=\"highlight\">postcode</b></i>?"
	elif ((not q.find("thomas") ==-1)or(not q.find("tom") ==-1)) and (not q.find("cool") == -1): #Suggested by alan - no egotism here.
		out="Yes."
	elif (("info" in q or "bio" in q) and len(q.split(" "))>1):
		name = " " + " ". join(q.split(" ")[1:])
		out = ("Information " * ("info" in q)) + ("Biography" * ("bio" in q) + "for" + name )

	else:
		out="Sorry, I didn't understand what you said.<br/> :("
else:
	out = "Please type a question in the box above."
print(out)