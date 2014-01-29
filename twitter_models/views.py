#! /usr/bin/env python

from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from twitter_models.models import *
from twitter_models.forms import *
from django.views.generic.edit import FormView
from django.db import connections, transaction
from django.http import Http404
from django.db import connection
import socket, errno, time
from pprint import pprint
from django.template.loader import get_template
from django.contrib.auth import logout
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.template import Context, Template
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime
from django.utils.timezone import utc

HOST = "localhost"
PORT = 5432
#CONTENT_SIZE = 10000
#TOPIC_SIZE = 1000
CONTENT_SIZE = 512
TOPIC_SIZE = 512
DBNAME = 'default'

def loginview(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

@login_required()
def home(request):
	html = myRender(request, 'base.html', {})
	return HttpResponse(html)

def auth_and_login(request, onsuccess='/home', onfail='/'):
	
	user = authenticate(username=request.POST['email'], password=request.POST['password'])
	if user is not None:
	    login(request, user)
	    return redirect(onsuccess)
	else:
	    return redirect(onfail)  

def user_exists(username):
	user_count = User.objects.filter(username=username).count()
	if user_count == 0:
		return False
	return True

def sign_up_in(request):
    post = request.POST
    if not user_exists(post['email']): 
        user = User.objects.create_user(username=post['email'], email=post['email'], password=post['password'])
    	return auth_and_login(request)
    else:
    	return redirect("/login/")

def logout_view(request):
	logout(request)
	return redirect("/")  
#def tabs(request):
#     return render_to_response('index.html')
#@login_required(login_url='/login/')
def post_tweet(request):
	if request.method == 'POST': # If the form has been submitted...
		username = request.user.username
		tweet = Tweet(username = username)
        	form = TweetForm(request.POST, instance=tweet) # A form bound to the POST data
		if form.is_valid():
	#	username = request.user.username
		#form.cleaned_data['username'] = username
	#	tweet = Tweet(username = username)
	#	print tweet.username
	#	tweet = form.save(commit=False)
	#	tweet.save()
			form.save()
			return redirect("/tweet/")
	else:
        	form = TweetForm() # An unbound form
		#form.fields['username'].initial = request.user.username
		return render(request, 'postTweet.html', {'form': form,})
@login_required(login_url='/login/')
def render_content(request, topic):
	content = dbfetchcontent(topic)
	return render(request, 'displayContent.html', { 'topic' : topic , 'content' : content })



# fetch all results of a SQL as a list of dicts
def dbfetchall(sql, params=[]):
	"Returns all rows from SQL query as a dict"
	global DBNAME
	cur = connections[DBNAME].cursor()
	cur.execute(sql)
	desc = cur.description
	return [
        	dict(zip([col[0] for col in desc], row))
	        for row in cur.fetchall()
	]

def addtoDB(sql):
	global DBNAME
	connections[DBNAME].autocommit = True
	cur = connections[DBNAME].cursor()
	cur.execute(sql)
	desc = cur.description
#	connections[DBNAME].commit()
	return 

@login_required
def displayTweets(request):
	username = request.user.username
	followers = getFollowers(username)
	#followers.append(username)
	followStr = usersToString(followers)
	tweets = getTweets(followStr)
	html = myRender(request, 'displayTweet.html', 
		{'tweets' :  tweets })
	return HttpResponse(html)
@login_required
def myTweets(request):
	username = request.user.username
	userStr = '(\''+username+'\')'
	tweets = getTweets(userStr)
	html = myRender(request, 'displayTweet.html', 
		{'tweets' :  tweets })
	return HttpResponse(html)


def getFollowers(username):
	followers = dbfetchall(
		"""
		SELECT following 
		FROM followers
		WHERE username LIKE '%s'
		""" % username
		)
	res = []
	res.append(username)
	for c in followers:
		res.append(c['following'])
	return res

def usersToString(followers):
	followStr = ''
	for i in followers:
		followStr = '\'' + i + '\','
	followStr = '(' + followStr[:-1] + ')'
	return followStr

def getTweets(usernames):
	sqlcmd = """
		SELECT username, content
		FROM tweets
		WHERE username IN %s
		ORDER BY timestamp
		""" % usernames
	print sqlcmd
	tweets = dbfetchall(sqlcmd)
	res = [{
		'username': c['username'],
		'content' : c['content']
		} for c in tweets]
	return res
##
# General function for rendering.
#
def myRender(request, template, context={}):
        t = get_template(template)
        c = RequestContext(request, context)
        return t.render(c)

@login_required(login_url='/login/')
def searchUsers(request):
	if request.method == 'POST': # If the form has been submitted...
		searchStr = request.POST['search']
		searchStr = searchStr.lower()
		sqlcmd = """
			SELECT username from auth_user
			WHERE username LIKE '%%""" + searchStr + """%%'
			""" 
		users = dbfetchall(sqlcmd)
		
		usernames = []
		for c in users:
			usernames.append(c['username'])
		html = myRender(request, 'subscribeUser.html', 
			{'users' : usernames })
		return HttpResponse(html)
	else:
		html = myRender(request, 'searchUser.html', {})
		return HttpResponse(html)
@login_required(login_url='/login/')
def subscribeUser(request, oid):
	username  = request.user.username
	follow = oid
	addtoDB(
		"""
		INSERT INTO followers(username, following)
		VALUES ('%s' , '%s')
		""" %(username, follow)
		)
	html = myRender(request, 'base.html')
	return HttpResponse(html)
#	return		
