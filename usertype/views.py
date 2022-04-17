from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from . import dbhelper
from .forms import LoginForm
from django.contrib.auth import authenticate, login

def admin(request):
	return render(request, 'usertype/admin.html)
def professor(request):
	return Hrender(request, 'usertype/professor.html)
def student(request):
	manager = dbhelper.dbManager()
	manager.connect('root','1234','university')
	feature_six_results = manager.getFeatureSix("CS", 1)
	context = {'feature_six_results':feature_six_results}
	return render(request, 'usertype/student.html', context)
def user_login(request):
	if request.method == 'POST': 
		form = LoginForm(request.POST)
		form.is_valid()
		user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
		if user is not None:
			login(request, user)
			user_type = user.groups.all()[0].name
			if user_type == 'Admin':
				return HttpResponseRedirect('admin')
			elif user_type == 'Professor':
				return HttpResponseRedirect('professor')
			elif user_type == 'Student':
				return HttpResponseRedirect('student')
	else:
		form = LoginForm()
		
	return render(request, 'usertype/login.html', {'form': form})
