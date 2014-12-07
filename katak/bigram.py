class BigramNode():
    nexts = None
    isBeginning = None

    def __init__(self):
        self.nexts = dict()
        self.isBeginning = False

    def addNext(self, token):
        if token in self.nexts:
            self.nexts[token] += 1
        else:
            self.nexts[token] = 1

    def getNexts(self):
        return self.nexts

class Bigram():
    nodeset = None
    bFile = None

    def __init__(self):
        self.nodeset = dict()

    def openBigram(self, bFile):
        import cPickle as pickle
        try:
            self.nodeset = pickle.load(open(bFile, "rb"))
        except:
            pass

        self.bFile = bFile

    def closeBigram(self):
        import cPickle as pickle

        pickle.dump(self.nodeset, open(self.bFile, "wb"))

    def insertToken(self, word_a, word_b, isBeginning=False):
        if word_a not in self.nodeset:
            self.nodeset[word_a] = BigramNode()
            self.nodeset[word_a].isBeginning = isBeginning
        self.nodeset[word_a].addNext(word_b)

    def nextWords(self, word):
        if word not in self.nodeset:
            raise Exception("Word not in bigram table.")

        total = 0
        wordNexts = self.nodeset[word].getNexts()
        for words in wordNexts:
            total += wordNexts[words]

        probabilities = []
        for key, value in wordNexts.items():
            probabilities.append((key, float(float(value)/float(total))))

        return probabilities

    def getRandomBeginning(self):
        import random

        beginningList = []
        for node in self.nodeset:
            if self.nodeset[node].isBeginning: beginningList.append(node)

        return random.choice(beginningList)
