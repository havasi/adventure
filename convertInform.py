# convertInform.py
# Some methods for letting common sense interacting with Inform --
# especially rewriting to handle ask about
# KG 4/20/11

import re

# makeMyRegex:  first group is name of person asked, second is list of topics
def makeMyRegex():
        return re.compile("After asking (?P<name>\w+) about \"(?P<topics>.+)\",")


# supplyAskTopics:  Assuming a dictionary from words to lists of 
#     other words (related topics), substitute relevant topics
#     into a given Inform line.
#
#     topicDict:  dictionary from words (strings) to lists of related words (also strings)
#     fileString:  A single line from the Inform file to check for replacement.
#     myRegex:  from makeMyRegex -- first group is person asked, second is topic list
def supplyAskTopics(topicDict,fileString,myRegex):
	patternMatch = myRegex.match(fileString)
	if (patternMatch == null):
		return fileString 	# most lines in file are unaffected
	personAsked = patternMatch.group(1)
	topicListText = patternMatch.group(2)
	topicList = re.split('[\W]+', topicListText)
	newTopicList = topicList.copy()
	for topic in topicList:
		topicLookup = topicDict[topic]
		for newtopic in topicLookup:
			newTopicList.append(newtopic)
	returnString = "After asking " + personAsked + " about \"" 
	firstTopic = true
	for newtopic in newTopicList:
		returnString += newtopic
		if (not firstTopic):
			returnString += "/"
		firstTopic = false
	returnString += "\","
	return returnString
