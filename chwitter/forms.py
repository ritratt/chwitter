from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
	username = forms.CharField(max_length = 100, label = 'Username')
	useremail = forms.EmailField()
	password = forms.CharField(widget = forms.PasswordInput(render_value = False), label = 'Password')

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 100, label = 'Username')
	password = forms.CharField(widget = forms.PasswordInput(render_value = False), label = 'Password')

class ChweetForm(forms.Form):
	chweeted = forms.CharField(max_length = 141, widget = forms.Textarea, label = 'Chweet')

class FollowForm(forms.Form):
	username = forms.CharField(max_length = 100)

class UnfollowForm(forms.Form):
        username = forms.CharField(max_length = 100)

class ListFollowForm(forms.Form):
	users = User.objects.all().values('username').order_by('username')
	user_list = []
	for user in users:
		user_list.append(user['username'])
	user_tuple = zip(user_list, user_list)
	userlist = forms.ChoiceField( 
        choices=user_tuple 
    	)
