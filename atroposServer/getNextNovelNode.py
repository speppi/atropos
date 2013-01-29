#!/usr/bin/python
import cgi
import json
import pygold

print "Content-type: text/json\n\n"

queryParams = cgi.FieldStorage()

if queryParams.has_key("choice") and queryParams["choice"].value !="":
	if (queryParams["choice"].value == "0"):
		data = {"$type": "DialogueNode, Assembly-CSharp", "dialogue":"You ain't half bad yourself!"}
	else:			
		data = {"$type": "DialogueNode, Assembly-CSharp", "dialogue":"Geez, you're makin me blush."}
	print json.dumps(data)
else:
	data = {"$type": "MenuNode, Assembly-CSharp", "choices":[ "You are cool", "You are suuuper cool" ]}
	print json.dumps(data)
