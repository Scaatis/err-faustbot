# -*- coding=utf-8 -*-

from errbot.botplugin import BotPlugin
from errbot import botcmd
import random

class FaustBot(BotPlugin):
    
    def __init__(self):
        super(FaustBot, self).__init__()
        self.parseFaust()
    
    def parseFaust(self):
        sentences = {}
        characters = {}
        # current line number
        i = 0
        # line the current sentence started in
        lastSentence = 0
        with open("faust.txt", encoding="utf-8") as faust:
            for line in faust:
                line = line[:-1] # remove \n
                if line.isupper():
                    characters[i+1] = [line[:-1].title()]
                elif line != "":
                    if line.startswith(" "): # this means the line is continued from another character
                        if lastSentence == 0:
                            lastSentence = self.getnextsmallerkey(sentences, i)
                        
                        # add the next speaking character
                        characters[lastSentence] = characters[self.getnextsmallerkey(characters, i)] + characters[i+1]
                    else:
                        i += 1
                    
                    if lastSentence == 0:
                        sentences[i] = line
                    else:
                        sentences[lastSentence] += " \\ " + line.lstrip()
                    
                    if line[-1] in ["!", ".", "?"] or (line[-1] == '"' and line[-2] in ["!", ".", "?"]):
                        lastSentence = 0
                    elif lastSentence == 0:
                        lastSentence = i
        
        self.sentences = sentences
        self.characters = characters
        self.lines = i
    
    @botcmd
    def faust(self, mess, args):
        """ Print a random line from Goethe's "Faust" in sentence context """
        argss = args.split()
        line = 0
        err = ""
        if len(argss) != 0:
            if argss[0] == "help":
                return "!faust für einen zufäigen Vers. !faust [1.." + str(self.lines) + "]\
 für einen bestimmten und !faust [-" + str(self.lines) + ",-1] für einen bestimmten von hinten."
            try:
                i = int(argss[0])
                if abs(i) > self.lines:
                    err += "Faust hat nur " + str(self.lines) + " Verse. Du kriegst einen anderen:\n"
                elif i == 0:
                    line = 1
                else:
                    if i < 0:
                        line = self.lines - i + 1
                    else:
                        line = i
            except ValueError:
                err += "Das ist keine Zahl. Ich bin mir sicher. Nimm einen zufälligen Vers:\n"
        
        if line == 0:
            line = random.randint(0, self.lines)
        
        whosaidit = self.getnextsmaller(self.characters, line)
        sentence = self.getnextsmaller(self.sentences, line)
        return err + '„{0}“, gesprochen von {1} in Vers {2}'.format(sentence, self.concat(whosaidit), line)
    
    def getnextsmaller(self, d, i):
        return d[self.getnextsmallerkey(d, i)]
    
    def getnextsmallerkey(self, d, i):
        last = -1
        for j in iter(sorted(d.keys())):
            if j > i:
                break
            last = j
        return last
    
    def concat(self, l):
        res = ""
        if len(l) == 0:
            return res
        res += l[0]
        for elem in l[1:-1]:
            res += ", " + elem
        if len(l) != 1:
            res += " und " + l[-1]
        return res
        
    def getlines(self):
        return self.lines