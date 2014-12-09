from django.shortcuts import render, redirect
from django.http import HttpResponse
from katak.bigram import *
from web.views import getSessionId
from Queue import Queue
from django.views.decorators.csrf import csrf_exempt
import re
import facebook

@csrf_exempt
def saveToken(request):
    request.session["facebook_token"] = request.POST.get("token")
    return HttpResponse("OK")

def trainPosts(request):
    graph = facebook.GraphAPI(request.session["facebook_token"])
    profile = graph.get_object("me")
    posts = graph.get_connections(profile['id'], 'posts')

    print posts

    for post in posts['data']:
        print post

    return HttpResponse("OK")