from django import forms
from twitter_models.models import *

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
#	exclude = ['username']

class UserTopicForm(forms.ModelForm):
    class Meta:
        model = UserTopic
        fields = ['userid', 'topic']
	exclude = ['userid']


