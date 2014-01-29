from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twitter.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'twitter_models.views.loginview'),
    url(r'^logout/$', 'twitter_models.views.logout_view'),
    url(r'^home/$', 'twitter_models.views.home'),
    url(r'^signup/', 'twitter_models.views.sign_up_in'),
    url(r'^auth/', 'twitter_models.views.auth_and_login'),
    #url(r'^$', 'twitter_models.views.render_topics'),
    #url(r'^tabs', 'twitter_models.views.render_topics'),
    #url(r'^home', 'twitter_models.views.render_topics'),
    url(r'^tweet', 'twitter_models.views.post_tweet'),
    url(r'^displaytweets', 'twitter_models.views.displayTweets'),
    url(r'^myTweets', 'twitter_models.views.myTweets'),
    url(r'^subscribeUser', 'twitter_models.views.searchUsers'),
    url(r'^subscribe/(?P<oid>.*)', 'twitter_models.views.subscribeUser'),	
   
    #url(r'^subscribeTopic', 'twitter_models.views.subscribe_topic'),
    #url(r'^topic/(?P<topic>.*)', 'twitter_models.views.render_content'),
)
