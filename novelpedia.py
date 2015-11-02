#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author Ozuru
@desc Submission for NaNoGenMo-2015
'''

import json, urllib2, re

#CONSTANTS below
RANDOM_ARTICLE_URL = "https://en.wikipedia.org/w/api.php?action=query&generator=random&grnnamespace=0&prop=extracts&explaintext&exintro&format=json" #URL to get a random Wikipedia article in JSON
CHAPTER_LENGTH = 2500 #length of a chapter, unimplemented as of v1
NOVEL_LENGTH = 55000 #word count to stop generating sentences at
NOVEL_FILE_NAME = "PythonManifesto.txt" #output file name


wordCount = 0 #counting variable
caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

FILE_HANDLER = open(NOVEL_FILE_NAME, 'w+')

def getRandomSentence(): #gets and returns the first sentence from a random Wikipedia article
    try:
        article = json.load(urllib2.urlopen(RANDOM_ARTICLE_URL))
        intro = ""
        for a in article['query']['pages']:
            intro = article['query']['pages'][a]['extract']
        firstSentence = split_into_sentences(intro)[0]
        return firstSentence
    except UnicodeEncodeError:
        print "Unicode encoding error!"
        return getRandomSentence()

def split_into_sentences(text): #regex magic
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

while wordCount < NOVEL_LENGTH: #main loop
    try:
        tempSentence = getRandomSentence() #grabs a random Wikipedia sentence
        tempLength = len(re.findall(r'\w+', tempSentence)) #tempLength = word count of tempSentence
        wordCount += tempLength #wordCount += word count of sentence
        FILE_HANDLER.write(tempSentence.encode('utf-8') + "\n") #writes the sentence to the file
        print "Added a sentence of " + str(tempLength) + " to the novel. Updated word count is " + str(wordCount)
        print tempSentence
        print "--------------------------------------"
    except Exception as e:
        print str(e)

FILE_HANDLER.close()
print "Word count is " + str(wordCount) + " so we are finished!"