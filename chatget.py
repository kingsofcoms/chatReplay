#OR: chatget.py [stream] [timeAt] [duration]
#cleans up and summarizes chat messages, output to d:/streamdata/chatvid for revision,


import sys,time
from fuzzywuzzy import fuzz

timeMergeDistance = 31.95			
timeMergeDistance = 99.95			
timeMergeDistance = 8.44
timeMergeDistance = 6.44			

#smaller merge intervals allow for more granular responses (great for when many events occur within a short space)
#large intervals are good for totaling response counts across the whole chat (great for when just one or few original thoughts are appearing in chat)

msgLen = 22
msgLen = 69
#maximum length messages allowed

blacklist = ["http","forsen","ᵃ","ᴇ","۞","⎠","📞","É","╣","tyler","sourpls","admiral","TOLI","","󀀀","贡","ȓ","񡠎","򬀀","ҏ"]

with open("D:/streamdata/banned") as banned:
	banned = banned.readlines()

banned = [x.strip() for x in banned]

with open("D:/streamdata/helpers") as helpers: #preferential treatment in displaying who wrote a message
	helpers = helpers.readlines()

helpers = [x.strip() for x in helpers]

args = sys.argv

	
try:
	stream = args[1]
	timeAt = float(args[2])
	duration = int(args[3])
	timeAt -= 76-4.56

except:
	print("Usage: chatget.py stream timeAt duration")
	exit()
	
fileName = "d:/streamdata/logout"

"""
if timeAt < 1502687762:
	fileName += "1"
"""
	
with open(fileName) as logout: #chat database
	logout = logout.readlines()
	
logout = [x.strip() for x in logout]

#chat storage format (from ripper/logout)
#		streamName$twitch username:message|seconds since epoch

errors = []
out = []

for chat in logout:
	
	
	if chat.split("$")[0] == stream:
		chat = chat.split("$")[1]
		if float(chat.split("|")[1]) > timeAt and float(chat.split("|")[1]) - timeAt < duration and chat.split(":")[0] not in banned and len(chat.split(":")[1].split("|")[0]) <msgLen:
			#extract messages within the time boundaries specified in sys.args
			#ignore messages from banned users
			#ignore messages that are too long
			yes = 1
			for word in blacklist:
				if word in chat.split(":")[1]:
					yes= 0
			if yes:
				out.append(chat)
mostPop = {}

for x in out:
	try:
		print(x)
	except:
		out.remove(x) #remove non utf-8 lines

		
for chat in out:
	try:
		mostPop[chat.split(":")[1].split("|")[0]] +=1 
	except:
		mostPop[chat.split(":")[1].split("|")[0]] =1 
alreadyChecked = []
	
while True:
	breaker = 1
	try:
		for ch in out:
			if ch not in alreadyChecked:
				for ch2 in out:
					if ch.split(":")[0] ==  ch2.split(":")[0] and fuzz.ratio(ch.split(":")[1].split("|")[0].lower(),ch2.split(":")[1].split("|")[0].lower()) > 55 and ch != ch2:
						if mostPop[ch.split(":")[1].split("|")[0]] > mostPop[ch2.split(":")[1].split("|")[0]]:#remove similar message spam from the same user
							out.remove(ch2)
						else:
							out.remove(ch)
						raise
				alreadyChecked.append(ch)
	except:
		breaker = 0
		
		pass
	if breaker:
		break
mostPop = {}

print("spam removed")

for chat in out:
	try:
		mostPop[chat.split(":")[1].split("|")[0]] +=1 
	except:
		mostPop[chat.split(":")[1].split("|")[0]] =1 

alreadyChecked = []
			
		
while True:
	breaker = 1
	try:
		for ch in out:
			if ch not in alreadyChecked:
				for ranked in mostPop:
					if (fuzz.ratio(ch.split(":")[1].split("|")[0], ranked) > 85 or fuzz.token_sort_ratio(ch.split(":")[1].split("|")[0], ranked) > 95) and mostPop[ranked] > mostPop[ch.split(":")[1].split("|")[0]]:
						out.append(( ch.split(":")[0] + ":"+ranked + "|" + ch.split("|")[1] )) # rank the most common spellings. change extremely similar messages to use the most common spelling (misspelling correction) 
						out.remove(ch)
						raise
				alreadyChecked.append(ch)
				
	except:
		breaker = 0
		pass
				
	if breaker:
		break
alreadyChecked = []
			
print("corrections made")


#todo: set time of popular messages to the average

while True:
	breaker = 1
	try:
		for ch in out:
			if ch not in alreadyChecked:
				for ch2 in out:						#merge identical messages, while displaying username list ranked by fastest reaction time (or by helper database), and counting unique users saying each unique message
					if ch.split("|")[0].split(":")[1].lower() == ch2.split("|")[0].split(":")[1].lower() and float(ch2.split("|")[1]) - float(ch.split("|")[1]) < timeMergeDistance and float(ch2.split("|")[1])-float(ch.split("|")[1]) >= 0 and ch != ch2:
						popCheck={}
						for chat in mostPop:
							if chat.lower() == ch.split(":")[1].split("|")[0].lower():
								popCheck[chat] = mostPop[chat]
						phrase = max(popCheck, key=popCheck.get)
						helper = ""
						helpSum = 0
						if ch2.split(":")[0] in helpers:
							helpSum += 1
							helper += ch2.split(":")[0] +", "
						if ch.split(":")[0] in helpers:
							helpSum += 1
							helper += ch.split(":")[0] + ", "
							
						if len( (ch.split(":")[0] + ", " +ch2.split(":")[0]) ) > 32 or "+" in ch.split(":")[0] or "+" in ch2.split(":")[0]:
							
							total = ch2.split(":")[0].count(",")
							total+= ch.split(":")[0].count(",")
							
							try:
								total += int(ch2.split(":")[0].split("+")[1])
							except:
								pass
							try:
								total += int(ch.split(":")[0].split("+")[1])
							except:
								pass
							if "," not in ch.split(":")[0]:
								total+= 1
							if "," not in ch2.split(":")[0]:
								total+= 1
								
							total -= helpSum
							
							if "+" in ch.split(":")[0]:
								out.append(( helper + ch.split("+")[0]  + "+" + str(total) + ":" +phrase + "|" + ch.split("|")[1] ))
							else:
								out.append(( helper + ch.split(":")[0]  + ", +" + str(total) + ":" +phrase + "|" + ch.split("|")[1] ))
						else:
							if ch.split(":")[0] in helper and ch2.split(":")[0] in helper or (ch.split(":")[0] not in helper and ch2.split(":")[0] not in helper):
								out.append(( ch.split(":")[0] + ", " +ch2.split(":")[0] +":" +phrase + "|" + ch.split("|")[1] ))
							elif ch.split(":")[0] in helper:
								out.append(( helper +ch2.split(":")[0] +":" +phrase + "|" + ch.split("|")[1] ))
							elif ch2.split(":")[0] in helper:
								out.append(( helper + ch.split(":")[0] +":" +phrase + "|" + ch.split("|")[1] ))
						
						out.remove(ch)
						out.remove(ch2)
						raise
				
				alreadyChecked.append(ch)
	except:
		breaker = 0
		pass
	if breaker:
		break


minBuffer = {}

for cmd in out:#sorting messages by time may no longer be required in python 3.6
	minBuffer[cmd.split("|")[0]] = float(cmd.split("|")[1])
	
print("similar messages within " + str(timeMergeDistance) + " seconds merged")
	
print(" - - - - - - - - - ")
with open("d:/streamdata/chatvid","w") as chatvid: #write chat to file, for further editing, and then video generation with chatvid.py
	while len (minBuffer) >0:
		cmd = min(minBuffer,key=minBuffer.get)
		
		cmd += "|"
		cmd +=str(minBuffer[min(minBuffer,key=minBuffer.get)])
		minBuffer.pop(min(minBuffer,key=minBuffer.get), None)
		cmd += "\n"
		chatvid.write(cmd)
		
		
		
		
		
		