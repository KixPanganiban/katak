from django.shortcuts import render, redirect
from django.http import HttpResponse
from katak.bigram import *
from web.views import getSessionId
from Queue import Queue
import re
import tweepy

def sendToAuth(request):
    """
    Redirects the user to the Twiter oAuth page.
    """
    auth = tweepy.OAuthHandler('Znumu9sLUUBdP0BIMKjonvzJN','sSaibMpTbcSjQwfWl1Rgl63uowZRiGdjysKxtJ4faf2L7Yxrs8')
    redirect_url = auth.get_authorization_url()
    request.session["twitter_request_token"] = auth.request_token
    return redirect(redirect_url)

def receiveAuth(request):
    """
    Callback view that receives the user from the Twitter
    oAuth page.
    """
    request.session["twitter_verifier"] = request.GET.get('oauth_verifier')
    return redirect("/")

def trainTweets(request):
    """
    Feeds the recent tweets from the authenticated user's timeline into
    the Markov Chain Bigram.
    """
    auth = tweepy.OAuthHandler('Znumu9sLUUBdP0BIMKjonvzJN','sSaibMpTbcSjQwfWl1Rgl63uowZRiGdjysKxtJ4faf2L7Yxrs8')
    auth.request_token = request.session["twitter_request_token"]
    auth.get_access_token(request.session["twitter_verifier"])

    api = tweepy.API(auth)
    tweets = api.user_timeline(count=3000)
    tweetStream = Queue()

    def readToken():
        """
        Get a token from the Queue.
        """
        if tweetStream.empty():
            return None
        return tweetStream.get()

    # Read the input stream
    for status in tweets:
        line = status.text

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

            tweetStream.put(tokenCleaned)

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

    bigram.closeBigram()
    request.session["twitter_trained"] = True

    return HttpResponse("OK")