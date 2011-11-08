#!c:\Python32\python.exe
import cgi
import csv
from math import floor
from lxml import etree
from urllib.request import urlopen, unquote, quote
from urllib.error import HTTPError
from string import punctuation
from sys import path
from json import loads
print ("Content-Type: text/html")
print  ()

form = cgi.FieldStorage()
out = ""
def AddCommas(integer):
	return "{:,}".format(int(integer))
def expenses(MPName):
	#Create CSV reader instance
	fil3 = csv.reader(open(path[0] + "/expenses.csv", "r"))
	rownum = -1
	i = 0
	for row in fil3:
		#See if it matches
		if ((row[2].split(" ")[-1] + " " + row[1]).lower() == MPName.lower()):
			return("Total expenses claimed 2007-2008: " + AddCommas(row[8])+" Pounds.<br/>")
			rownum = i
			break
		i +=1
	#check for problems
	if(rownum == -1):
		return("")
def doddsid(twfyid):
	mappings = open(path[0]+ "\mappings.txt", "r")
	for line in mappings:
		if (str(twfyid) == line.split(",")[1]):
			return int(line.split(",")[0])
	return ""
def Bioid(twfyid):
	mappings = open(path[0]+ "\mappings.txt", "r")
	for line in mappings:
		if (str(twfyid) == line.split(",")[1]):
			return int(line.split(",")[2])
	return ""
def bdp(tag):
	 return bio_data.xpath("//biography:%s/text()" % tag, namespaces={"biography":"http://www.parliament.uk/xmlns/metadata/member/2011/01/biography/"})
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
		con3 = urlopen("http://www.theyworkforyou.com/api/getMPInfo?id=" + data["person_id"] +"&fields=register_member_interests_html&output=json&key=DiEfMMDNP6g6EGaNC4AN4Lwb")
		#Parse JSON
		moredata = loads(con3.read().decode())
		#Be kinder to servers
		con3.close()
		#Open the Parliament Biographical Data
		problem = False
		try:
			con2 = urlopen("http://data.parliament.uk/resources/members/api/biography/" + str(Bioid(data["person_id"]) ) + "/")
			#Create a new parser class as our means
			parser = etree.XMLParser(ns_clean=True)
			#Create a parsing XML object containing the data
			bio_data = etree.parse(con2, parser)
			#Define some stuff
			comit = bdp("committeeName")
			website = bdp("website")
		except HTTPError:
			problem = True
		#Construct their name
		full_name = " ".join([data['title'], data['first_name'], data['last_name']])
		#Start generating the page
		if (problem):
				out = """
			<h3><b class="highlight">%s</b> &mdash; %s MP for %s</h3><br />
			<div id="details">
			<img style="float:left; margin:5px; /*margin-left:-%spx;*/border: 3px solid #%s;border-radius:15px;"src="%s" alt="%s"/>
			Could not find the Bio for this MP. Some information may be missing.
			Email: %s<br/>
			%s
			Telephone: %s<br/>
			Fax: %s<br/>
			%s
			%s
			%s
			<span id="ints" style="font-size:12px;">%s</span>
			<br/><small>ID Numbers: twfy #%s Biography #%s Dodds #%s</small>
			</div>
			""" % (
				full_name,
				data['party'],
				data['constituency'],
				data["image_width"],
				"FFFFFF",
				"",
				full_name, "",
				"", #Todo: fill these with twfy data
				"",
				"",
				"",
				"",
				expenses(data["first_name"] + " " + data["last_name"]),
				moredata["register_member_interests_html"],
				data['person_id'], Bioid(data["person_id"]), doddsid(data["person_id"])
				)
		else:
			out = """
		<h3><b class="highlight">%s</b> &mdash; %s MP for %s</h3><br />
		<div id="details">
			<img style="float:left; margin:5px; /*margin-left:-%spx;*/border: 3px solid #%s;border-radius:15px;"src="%s" alt="%s"/>
			Email: %s<br/>
			%s
			Telephone: %s<br/>
			Fax: %s<br/>
			%s
			%s
			%s
			<span id="ints" style="font-size:12px;">%s</span>
			<br/><small>ID Numbers: twfy #%s Biography #%s Dodds #%s</small>
		</div>
		""" % (
				full_name,
				data['party'],
				data['constituency'],
				data["image_width"],
				bdp("colour")[0],
				bdp("lowResPhoto")[0] if len(bdp("lowResPhoto")) >0 else "",
				full_name, bdp("email")[0],
				"Website: " +", ".join(website)+ ".<br/>" if len(website) > 0 else "",
				bdp("phone")[0],
				bdp("fax")[0],
				"Comittee: " +", ".join(comit)+ ".<br/>" if len(comit) > 0 else "",
				"Post: " + ", ".join(bdp("postName")) + ".<br/>" if len(bdp("postName")) > 0 else "",
				expenses(data["first_name"] + " " + data["last_name"]),
				moredata["register_member_interests_html"],
				data['person_id'], Bioid(data["person_id"]), doddsid(data["person_id"])
				)
			con2.close()
	elif  ( ( (not q.find("mp") == -1) and (not q.find("who") == -1 ) )  and (q.find("for") ==-1)):
		out ="If you're looking for your MP, ask: <i>Who is the mp for <b class=\"highlight\">postcode</b></i>?"
	elif ((not q.find("thomas") ==-1)or(not q.find("tom") ==-1)) and (not q.find("cool") == -1): #Suggested by alan - no egotism here.
		out="Most certianly yes."
	else:
		out="Sorry, I didn't understand what you said.<br/> :("
else:
	out = "Please type a question in the box above."
print(out)