from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from chwitter.forms import *
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from userdata.models import Chweets, Following

def home(request):
	''' Home page i.e. Login Page.'''
	try:
		#Check REG flag and LOGOUT flag then set special message accordingly.
		if request.session['REG']:
			request.session['specialmsg'] = 'Registration successful! Please login to proceed.'
			request.session['REG'] = False
		elif request.session['LOGOUT']:
			request.session['specialmsg'] = 'You have been successfully logged out.'
			request.session['LOGOUT'] = False
		else:
			request.session['specialmsg'] = ''

	except KeyError:
		try:
			if request.session['LOGOUT']:
				request.session['specialmsg'] = 'You have been successfully logged out.'
				request.session['LOGOUT'] = False
			else:
				request.session['specialmsg'] = ''
		except KeyError:
			request.session['REG'] = False
			request.session['LOGOUT'] = False
			request.session['specialmsg'] = ''		#Flag checking and special message setting end here.

	if request.method == 'POST':
		form = LoginForm(request.POST)
		request.session['registration'] = ''
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = auth.authenticate(username = username, password = password)
			if user and user.is_authenticated():
				auth.login(request, user)
				return HttpResponseRedirect('/userpage')
			else:
				return HttpResponse('Incorrect/Non-existent credentials.')
	else:
		form = LoginForm()
	return render_to_response('home.htm', {'form':form, 'special_message':request.session['specialmsg']}, context_instance = RequestContext(request))

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			useremail = form.cleaned_data['useremail']
			password = form.cleaned_data['password']
			user = User.objects.create_user(username = username, password = password)
			user.save()
			loginform = LoginForm()
			request.session['REG'] = True	#Set REG flag for special message on home page.
	
			#Create row in Following table to follow self so that all self chweets also display in feed.
			follow_self = Following(user = username, following = username)
			follow_self.save()
			return HttpResponseRedirect('/')
	else:
		form = RegisterForm()
	return render_to_response('register.htm', {'form':form}, context_instance = RequestContext(request))

def userpage(request):
	
	#These three variables are used later for displaying some informative errors to the user.
	follow_error = ''
	request.session['following_msg'] = ''
	request.session['nochweets_msg'] = ''

	username = request.user.username

	#Get users being followed and display accordingly. Must create separate module and put in it as a function.
	users = Following.objects.filter(user = username).values('following')
	following_users = []
	for user in users:
		following_users.append(user['following'])
	if not following_users:
		request.session['following_msg'] = 'You are currently not following anyone.'

	#Get chweets from everyone the user follows and put then in a list. Must put in module too.
	chweetstodisplay = []
	chweeters = []
	raw_chweets = Chweets.objects.filter(user__in=following_users).values('user', 'chweet').order_by('-timestamp')
	for chweet in raw_chweets:
		chweetstodisplay.append(chweet['user'] + ' chweeted: ' + chweet['chweet'])
		#chweeters.append(chweet['user'])
	if not chweetstodisplay:
		request.session['nochweets_msg'] = 'No latest chweets from followers...'
	else:
		chweetstodisplay = chweetstodisplay[:10]
		chweeters = chweeters[:10]

	#Start POSTing.
	if request.method == 'POST':
		#Check which form was submitted using POST data.
		if 'chweet' in request.POST:
			form_chweet = ChweetForm(request.POST)
			if form_chweet.is_valid():
				chweet = form_chweet.cleaned_data['chweeted']
				chrow = Chweets(user = request.user.username, chweet = chweet)
				chrow.save()
		elif 'follow' in request.POST:
			form_follow = FollowForm(request.POST)
			if form_follow.is_valid():
				username_follow = form_follow.cleaned_data['username']
				if User.objects.filter(username = username_follow).count():	#Check through try if user already follows the given user. If so set follow_error accordingly.
					try:
						dup_check = Following.objects.get(user = request.user.username, following = username_follow)
						follow_error = 'You are already following ' + username_follow + '.'
					except Following.DoesNotExist:	#This exception means no such row exists which means not following the given user.
						frow = Following(user = request.user.username, following = username_follow)
						frow.save()
						follow_error = 'You are now following ' + username_follow + ' !'
				else:
					follow_error = 'User not found.'
		elif 'logout' in request.POST:
			auth.logout(request)
			request.session['LOGOUT'] = True
			return HttpResponseRedirect('/')
	form_chweet = ChweetForm()
	form_follow = FollowForm()
	return render_to_response('userpage.htm', {'form_chweet':form_chweet, 'form_follow':form_follow, 'users':following_users, 'follow_error':follow_error, 'following_msg':request.session['following_msg'], 'chweets':chweetstodisplay
}, context_instance = RequestContext(request))
