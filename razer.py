#!/usr/bin/python

print "Content-type:text/html\r\n\r\n"
import cgi, cgitb, sys, random, time, feedparser

form = cgi.FieldStorage()

numChoice = form.getvalue('how_many_headlines')
numChoice = int(numChoice)
joinChoice  = form.getvalue('what_joiner_word')
joinChoice = joinChoice.upper()
newFileChoice = form.getvalue('update_file')

startProgram = time.clock()

flag = False
inFront, inBack = [], []
chosenIndexA, chosenIndexB = 0, 0


print '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="apple-mobile-web-app-capable" content="yes" />
	<title>RAzer</title>
	<style type="text/css">
		p { font-family: "helvetica neue", arial, sans-serif; font-weight: 300; margin-bottom: -8px; }
		.list { padding-top: 5px; padding-left: 40px; padding-bottom: 10px; }
		h2 { font-size: 3.4em; font-family: "helvetica neue", arial, sans-serif; margin-bottom: 50px; color: white; position: relative; top: 13px;}
		.main { padding: 20px; font-size: .8em; }
		h4 { font-family: "helvetica neue", arial, sans-serif; }
		body { background-image: url("http://lorempixel.com/400/200"); background-size: 100% 60px; background-repeat: no-repeat; position: relative; bottom: 60px; }
	</style>
</head>

<body>
<div class="main">
<h2>RAzer</h2>
<h4>A headline cutup program by <a href="http://generaleccentric.net">Michael LeBlanc</a></h4>
'''
#  Retrieve headlines from text file

headlines = []

feeds = ['http://www.theglobeandmail.com/news/national/?service=rss','http://rss.cbc.ca/lineup/offbeat.xml','http://rss.cbc.ca/lineup/topstories.xml','http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml','http://www.thestar.com/feeds.topstories.rss','http://feeds.reuters.com/Reuters/worldNews?format=xml','http://feeds.bbci.co.uk/news/rss.xml?edition=int', 'http://www.npr.org/rss/rss.php?id=1020','http://www.ft.com/rss/world/us/society','http://feeds2.feedburner.com/ft/the-world','http://www.forbes.com/real-time/feed2/','http://feeds.feedburner.com/haaretz/LBao']

if newFileChoice == 'on':

    fo = open('latestheadlines.txt', 'w')

    for i in feeds:
        d = feedparser.parse(i)
        for post in d.entries:  
            pt = post.title.encode('utf-8') + '\n'
            fo.write(pt)
    fo.close()

    
fo = open('latestheadlines.txt', 'r')    
        
#  Build a list of headlines
for line in fo:
    line = line.replace('\n', '')      # remove linefeeds
    line = line.upper()
    headlines = headlines + [line]     # add headline to list  
fo.close()


#  Step through headlines, making new list from words in front of conjunction
  
for line in headlines:              # step through each headline
    
    headlineWords = line.split()      # split each headline into words

#  Look for headlines that have an occurence of the join word:
#  The join word must be present in the headline, 
#  AND there must be only one occurrence of the join word, 
#  AND the join word must not be the first word in the list.
  
    if joinChoice in headlineWords and headlineWords.count(joinChoice) == 1 and str(headlineWords[0]) != joinChoice:
        
        idx = 0                                # init index of words in list
        headline, front, back = '', '', ''     # empty strings
        mids = int(headlineWords.index(joinChoice))

        for words in headlineWords:  # reconstitute list words to a string
            if words == joinChoice:
                flag = True
            elif words != joinChoice and flag == False:
                front = front + headlineWords[idx] + ' '
                idx += 1
            elif words != joinChoice and flag == True:
                idx += 1
                back = back + headlineWords[idx] + ' '
        flag = False

#  Create a front and back list of phrases that straddle the join word
        inFront = inFront + [front]   # list of front phrases for all join words
        inBack = inBack + [back]      # list of back phrases for all join words

#  Now, the final event: choose at random one front and one back
numberOfHeadlines = len(inFront) - 1

print '<p>Source headlines for joiner word "{}": {}</p>' .format(joinChoice, numberOfHeadlines)

print '<div class="list">'

ex = 1        # initialize new headline index number

#  Run through this a number of times
for x in range(0, numChoice):

#  Choose random front and back segments of headline
    chosenIndexA = random.randrange(0, numberOfHeadlines)
    chosenIndexB = random.randrange(0, numberOfHeadlines)

#  To ensure that the front and back of the new cutup are not from the same headline--
#  which would defeat the purpose of the program--in other words,
#  if the index number is the same for A and B, choose B again
    if chosenIndexA == chosenIndexB:
        chosenIndexB = random.randrange(0, numberOfHeadlines)
  

#  Assemble front & back segments according to joiner word choice
    if joinChoice == 'IN':
        theText = inFront[chosenIndexA] + 'IN ' + inBack[chosenIndexB]
    elif joinChoice == 'ON':
        theText = inFront[chosenIndexA] + 'ON ' + inBack[chosenIndexB]
    elif joinChoice == 'OF':
        theText = inFront[chosenIndexA] + 'OF ' + inBack[chosenIndexB]
    elif joinChoice == 'THE':
        theText = inFront[chosenIndexA] + 'THE ' + inBack[chosenIndexB]    
    elif joinChoice == 'FOR':
        theText = inFront[chosenIndexA] + 'FOR ' + inBack[chosenIndexB]
    elif joinChoice == 'AT':
        theText = inFront[chosenIndexA] + 'AT ' + inBack[chosenIndexB]
    elif joinChoice == 'TO':
        theText = inFront[chosenIndexA] + 'TO ' + inBack[chosenIndexB]
    elif joinChoice == 'INTO':
        theText = inFront[chosenIndexA] + 'INTO ' + inBack[chosenIndexB]
    elif joinChoice == 'AS':
        theText = inFront[chosenIndexA] + 'AS ' + inBack[chosenIndexB]
    elif joinChoice == 'FROM':
        theText = inFront[chosenIndexA] + 'FROM ' + inBack[chosenIndexB]
    elif joinChoice == 'OVER':
        theText = inFront[chosenIndexA] + 'OVER ' + inBack[chosenIndexB]

  
#  Print it    
    if ex < 10:    # if index number is less than 10, add leading zero
        print '<p>0{}: {}</p>' .format(ex, theText)
    else:
        print '<p>{}: {}</p>' .format(ex, theText)
    ex += 1

#print ''    # Add a linefeed at the end!


print '</div>'

endProgram = time.clock()
executionTime = endProgram - startProgram
print "<p>Time to execute: {} seconds</p>" .format(executionTime)

print '\n<p><strong><a href="http://ahclem.is-leet.com/razercgi.html">Return to Input Form</a></strong></p>'



#print '<p>Headlines requested: %d</p>' % (numChoice)
#print '<p>Joiner word: %s</p>' % (joinChoice)
#if newFileChoice == "on":
#    print '<p><strong>UPDATE HEADLINE FILE</strong></p>'

print '</div>'	
print '</body>'
print '</html>'
