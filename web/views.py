from django.shortcuts import render, redirect
from django.http import HttpResponse
from katak.models import *
from katak.bigram import *
from forms import CorpusForm
from Queue import Queue
import re
import random
import string

def getSessionId(request):
    return request.session["sessionId"]

def home(request):
    if "sessionId" not in request.session:
        request.session["sessionId"] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    return render(request, "home.html", {
        "corpusFiles": CorpusFile.objects.filter(owner=getSessionId(request)),
        "sessionId": getSessionId(request),
        "twitter": True if "twitter_verifier" in request.session else False,
        "twitter_trained": True if "twitter_trained" in request.session else False
        })

def uploadCorpus(request):
    corpusForm = CorpusForm(request.POST, request.FILES)
    if corpusForm.is_valid():
        newCorpus = CorpusFile(
            corpusFile = request.FILES['corpusFile'],
            fileName = request.FILES['corpusFile'].name,
            owner = getSessionId(request)
            )
        newCorpus.save()
    else:
        return HttpResponse("Invalid file! Please try again!")

    return redirect("/")

def trainCorpus(request):
    try:
        corpusFile = CorpusFile.objects.get(id=request.GET.get("fileId"))
        corpusFilePath = corpusFile.corpusFile.path
    except:
        return HttpResponse("Invalid file id.")

    corpusStream = Queue()

    def readToken():
        if corpusStream.empty():
            return None
        return corpusStream.get()

    # Read the input stream
    with open(corpusFilePath, "r") as cfOpen:
        while 1:
            line = cfOpen.readline()
            if not line: break

            for whitespace in ["\n", "    ", "\t", "\r"]:
                line = line.replace(whitespace, " ")

            lineArray = line.split(" ")
            for token in lineArray:
                # Remove URLs
                if re.match("^https?\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$", token): continue

                # Eliminate hashtags an @mentions
                if len(token) > 1 and token[0] in ["#", "@"]: continue

                tokenCleaned = re.sub("[^A-Za-z!?\.,-]", "", token)
                if tokenCleaned == "" or unicode(tokenCleaned).isnumeric(): continue

                corpusStream.put(tokenCleaned)

    # Train the corpus to the bigram
    bigram = Bigram()
    bigram.openBigram("%s.b"%(getSessionId(request)))

    punctuations = [".", "!", "?"]
    token = readToken()
    terminated = True

    while 1:
        if not token:
            break

        tokenNext = readToken()

        if tokenNext:
            bigram.insertToken(token, tokenNext, terminated)
            terminated = True if token[-1] in punctuations else False
            token = tokenNext
        else:
            bigram.insertToken(token, "\n", terminated)
            terminated = True
            token = readToken()

    corpusFile.trained = True
    corpusFile.save()

    bigram.closeBigram()

    return HttpResponse("OK")


def generateString(request):
    bigram = Bigram()
    bigram.openBigram("%s.b"%(getSessionId(request)))
    try:
        def getNext(word, bigram):
            def weighted_choice(choices):
                """
                Randomly chooses a word from a list of word-probability pairs.
                http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
                """
                import random

                total = sum(w for c, w in choices)
                r = random.uniform(0, total)
                upto = 0
                for c, w in choices:
                   if upto + w > r:
                      return c
                   upto += w
                assert False, "Shouldn't get here"

            nextWords = bigram.nextWords(word)
            return weighted_choice(nextWords)

        punctuations = [".", "!", "?"]
        outputString = []
        inWord = bigram.getRandomBeginning()

        while (inWord and inWord != "\n"):
            outputString.append(inWord)
            if inWord[-1] in punctuations: break

            inWord = getNext(inWord, bigram)
    except:
        return HttpResponse("No data yet.")

    return HttpResponse(" ".join(outputString))