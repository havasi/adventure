# convertInform.py
# Some methods for letting common sense interacting with Inform --
# especially rewriting to handle ask about
# KG 4/20/11

import re

# makeMyRegex:  first group is name of person asked, second is list of topics
def makeMyRegex():
        return re.compile("After asking (?P<name>[\w|\W]+) about \"(?P<topics>.+)\"(?P<rest>.+)")

# makeSubjectRegex:  for Glass.  
# To decide which sentence type to output, we'll make 3 separate
# regexes, and run them individually.
def makeSubjectRegex():
	# Breaking this into parts to wrap my head around it
	return re.compile("([\w| ]+) is a subject.")

# makeSuggestsRegex: for Glass again -- also gets subjects.
def makeSuggestsRegex():
	return re.compile("([\w| ]+) suggests ([\w| ]+)")

# makeUnderstandsRegex: Again, 3rd type of subject-introducing sentence.
# ?: makes a group non-capturing.  
def makeUnderstandsRegex():
	return re.compile("Understand \"([\w| ]+)\"( or \"([\w| ]+)\")* as ([\w| ]+).")

# makeBoatloadOfUnderstandsRegexes: Since regexes don't quite work the way we want,
# we're going to unroll the cases, and store them in a list.
#
# This is so dumb.
def makeBoatloadOfUnderstandsRegexes():
	regexList = []
	for i in range(0, 20):
		regexText = "Understand \"([\w| ]+)\""
		for j in range(0,i):
			regexText += " or \"([\w| ]+)\""
		regexText += " as ([\w| ]+)."
		print regexText
		regexList.append(re.compile(regexText))
	return regexList

# supplyAskTopics:  Assuming a dictionary from words to lists of
#     other words (related topics), substitute relevant topics
#     into a given Inform line.
#
#     topicDict:  dictionary from words (strings) to lists of related words (also strings)
#     fileString:  A single line from the Inform file to check for replacement.
#     myRegex:  from makeMyRegex -- first group is person asked, second is topic list
def supplyAskTopics(topicDict,fileString,myRegex):
        patternMatch = myRegex.match(fileString)
        if (patternMatch == None):
                return fileString       # most lines in file are unaffected
	print 'merp'
        personAsked = patternMatch.group(1)
        topicListText = patternMatch.group(2)
        topicList = re.split('[\W]+', topicListText)
        newTopicList = []
	newTopicList.extend(topicList)
        for topic in topicList:
		if topic in topicDict:
                	topicLookup = topicDict[topic]
                	for newtopic in topicLookup:
                        	newTopicList.append(newtopic)
        returnString = "After asking " + personAsked + " about \""
        firstTopic = True
        for newtopic in newTopicList:
                if (not firstTopic):
                        returnString += "/"
                returnString += newtopic
                firstTopic = False
	returnString += "\""
	rest = patternMatch.group(3)
	returnString += rest
        return returnString

# Emily Short's glass:  different regex, but same basic idea.
# Because there's no name of a person, and the output is different,
# not much code above can be reused.
#
# topicDict:  topic-to-list-of-topics dictionary.
# line: single line of text
# regexes: one per sentence type we might be interested in
#
# This will pull the whole list of topics for the file, before any synonyms are added.
# This will avoid clobbering existing synonyms and understand statements.
def getEmilyShortTopics(text, subjectRegex, suggestsRegex):
	topicList = []
	finditer = subjectRegex.finditer(text)
	for match in finditer:
		topicList.append(match.group(1).strip())
	finditer = suggestsRegex.finditer(text)
	for match in finditer:
		topicList.append(match.group(1).strip())
		topicList.append(match.group(2))
	# I think we'll handle understands slightly differently
	# to successfully map things to the subjects instead of
	# their synonyms
	return topicList

# getEmilyShortUnderstands:  pass in our boatload of regexes
def getEmilyShortUnderstands(text, understandRegexes):
	# subjectMap: we will want to make Understand x as y
	# map the new topics to y, not x
	# map is from related stuff to the topic
	subjectMap = {}
	for understandRegex in understandRegexes:
		finditer = understandRegex.finditer(text)
		for match in finditer:
			topic = match.group(match.lastindex)
			for i in range(1, match.lastindex):
				relatedTopic = match.group(i).strip()
				subjectMap[relatedTopic] = topic
	return subjectMap

def supplyUnderstandText(topicDict, understandMap):
	extraText = ""
	topicList = topicDict.keys()
	alreadyAdded = []
	alreadyAdded.extend(topicList)
	understandKeys = understandMap.keys()
	for topic in topicList:
		relatedTopics = topicDict[topic]
		if not relatedTopics == None:
			for relatedTopic in relatedTopics:
				# Avoid mixing up things already topics/understands
				if not relatedTopic in alreadyAdded:
					# Let's keep things simple -- one line
					# per "understand"
					if not topic in understandKeys:
						extraText += "Understand \"" + relatedTopic + "\" as " + topic + ".\n"
					else:
						extraText += "Understand \"" + relatedTopic + "\" as " + understandMap[topic] + ".\n"
					alreadyAdded.append(relatedTopic)
	return extraText

# topicList:  a simple wrapper for the understands/topics stuff
def pullAllTopics(filename):
	text = ""
	file = open(filename, 'r')
	for line in file:
		text += line 
	file.close()
	subjectRegex = makeSubjectRegex()
	suggestsRegex = makeSuggestsRegex()
	topicList = getEmilyShortTopics(text, subjectRegex, suggestsRegex)
	understandsRegexes = makeBoatloadOfUnderstandsRegexes():
	understandDict = getEmilyShortUnderstands(text, understandRegexes):
	topicList.extend(understandDict.keys())
	return topicList

# convertFile:  This is the workhorse, to be run on an Inform file.
# Must pass in the topic dictionary.
#def convertFile(topicDict, filename, newFilename):
#	output = ""
#	myRegex = makeMyRegex()
#	file = open(filename, 'r')
#	for line in file:
#		output += supplyAskTopics(topicDict,line,myRegex)
#	file.close()
#	file = open(newFilename, 'w')
#	file.write(output)
#	file.close()
