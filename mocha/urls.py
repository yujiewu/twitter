from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mocha.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'mocha_models.views.loginview'),
    url(r'^home/$', 'mocha_models.views.home'),
    url(r'^signup/', 'mocha_models.views.sign_up_in'),
    url(r'^auth/', 'mocha_models.views.auth_and_login'),
    #url(r'^$', 'mocha_models.views.render_topics'),
    #url(r'^tabs', 'mocha_models.views.render_topics'),
    #url(r'^home', 'mocha_models.views.render_topics'),
    url(r'^tweet', 'mocha_models.views.post_tweet'),
    url(r'^displaytweets', 'mocha_models.views.displayTweets'),
    url(r'^myTweets', 'mocha_models.views.myTweets'),
    url(r'^subscribeUser', 'mocha_models.views.searchUsers'),
	
    #url(r'^subscribeTopic', 'mocha_models.views.subscribe_topic'),
    #url(r'^topic/(?P<topic>.*)', 'mocha_models.views.render_content'),
)
