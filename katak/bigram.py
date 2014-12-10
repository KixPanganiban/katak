class BigramNode():
    """
    Bigram node object that holds the pointers to the next
    Bigram nodes and their respective counts.
    """
    nexts = None
    isBeginning = None

    def __init__(self):
        self.nexts = dict()
        self.isBeginning = False

    def addNext(self, token):
        """
        Create a new next pointer or add +1 to the counter if it already
        exists.
        """
        if token in self.nexts:
            self.nexts[token] += 1
        else:
            self.nexts[token] = 1

    def getNexts(self):
        """
        Get the pointers and weights to the next bigram nodes.
        """
        return self.nexts

class Bigram():
    """
    Bigram 'root' that holds the pointers to the bigram nodes.
    Unique for every user session and is serialized through pickling.
    """
    nodeset = None
    bFile = None

    def __init__(self):
        self.nodeset = dict()

    def openBigram(self, bFile):
        """
        Load data from serialized pickle file.
        """
        import cPickle as pickle
        try:
            self.nodeset = pickle.load(open(bFile, "rb"))
        except:
            pass

        self.bFile = bFile

    def closeBigram(self):
        """
        Serialize data to pickle file.
        """
        import cPickle as pickle

        pickle.dump(self.nodeset, open(self.bFile, "wb"))

    def insertToken(self, word_a, word_b, isBeginning=False):
        """
        Takes two tokens, and adds the second one as a next pointer
        to the first one.
        """
        if word_a not in self.nodeset:
            self.nodeset[word_a] = BigramNode()
            self.nodeset[word_a].isBeginning = isBeginning
        self.nodeset[word_a].addNext(word_b)

    def nextWords(self, word):
        """
        Gets the next pointers plus counts of a given token.
        """
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
        """
        Randomly choose a token from the bigram which is flagged as a beginning of a sentence.
        """
        import random

        beginningList = []
        for node in self.nodeset:
            if self.nodeset[node].isBeginning: beginningList.append(node)

        return random.choice(beginningList)
