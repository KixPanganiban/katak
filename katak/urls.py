from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'web.views.home', name='home'),
    url(r'^corpus/upload/$', 'web.views.uploadCorpus', name='uploadCorpus'),
    url(r'^corpus/train/$', 'web.views.trainCorpus', name='trainCorpus'),
    url(r'^markov/generate/$', 'web.views.generateString', name='generateString'),
    url(r'^twitter/send/$', 'twitter.views.sendToAuth', name='sendToAuth'),
    url(r'^twitter/receive/$', 'twitter.views.receiveAuth', name='receiveAuth'),
    url(r'^twitter/train/$', 'twitter.views.trainTweets', name='trainTweets'),
    url(r'^facebook/savetoken/$', 'facebookapp.views.saveToken', name='saveToken'),
    url(r'^facebook/train/$', 'facebookapp.views.trainPosts', name='trainPosts'),
)
