from django import forms

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
