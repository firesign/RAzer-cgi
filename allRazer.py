#!/usr/local/bin
# -*- coding: utf-8 -*-

#==================================
#
#   allRazer : 
#   Traverse list of headlines, looking for words such as
#   "in", "to", "into", "of", "as", "over", "from", "on", "as".
#   If found, save the words up to that point as 'front', then search in successive
#   headlines for other instances of the found joining word. Save the words from this 
#   point to the end of the list as "back"
#   Put front + joining word + back together to form new cutup!
#
#   by Michael LeBlanc mleblanc@nscad.ca
#   August 2014
# 
#==================================


import sys, random, time, feedparser


#headlines = []

    



def main():

#  User input
    print ''
    print '\/\/\/\/ allRazer.py \/\/\/\/' + '\n'
    numChoice = raw_input('How many headlines? : ')
    numChoice = int(numChoice)
    joinChoice = raw_input('What joiner word (in/on/for/of/the/at/to/into/as/from/over)? : ')
    joinChoice = joinChoice.upper()     # convert to uppercase

    print ''
    
    newFileChoice = raw_input('Do you want to update the news headlines textfile? y/n: ')
  
    startProgram = time.clock()

    flag = False
    inFront, inBack = [], []
    chosenIndexA, chosenIndexB = 0, 0

#  Retrieve headlines from text file

    headlines = []
    
    print ''
    print '******************************************'
      
    feeds = ['http://www.theglobeandmail.com/news/national/?service=rss','http://rss.cbc.ca/lineup/offbeat.xml','http://rss.cbc.ca/lineup/topstories.xml','http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml','http://www.thestar.com/feeds.topstories.rss','http://feeds.reuters.com/Reuters/worldNews?format=xml','http://feeds.bbci.co.uk/news/rss.xml?edition=int', 'http://www.npr.org/rss/rss.php?id=1020','http://www.ft.com/rss/world/us/society','http://feeds2.feedburner.com/ft/the-world','http://www.forbes.com/real-time/feed2/','http://feeds.feedburner.com/haaretz/LBao']
    
    print "Saving feeds to text file"
    
    if newFileChoice == 'y':

        fo = open('latestheadlines.txt', 'w')
    
        for i in feeds:
            d = feedparser.parse(i)
            for post in d.entries:  
                pt = post.title.encode('utf-8') + '\n'
                fo.write(pt)
        fo.close()
    
    print "Building headline list\n"
        
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

        f = []                            # f = empty list

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
    
    print "NumberOfHeadlines: {}\n" .format(numberOfHeadlines)
  
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
            print '0{}: {}' .format(ex, theText)
        else:
            print '{}: {}' .format(ex, theText)
        ex += 1
    
    print ''    # Add a linefeed at the end!

    endProgram = time.clock()
    executionTime = endProgram - startProgram
    print "Time to execute: {} seconds\n" .format(executionTime)
  


if __name__ == '__main__':
    main()
