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
)
