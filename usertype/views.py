from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from . import dbhelper
from .forms import LoginForm
from django.contrib.auth import authenticate, login


def admin(request):
    return render(request, 'usertype/admin.html')


def professor(request):
    return render(request, 'usertype/professor.html')


def student(request):

    classes = {}
    context = {'list': classes}
    if (request.method == 'POST'): #https://www.etutorialspoint.com/index.php/257-django-pass-variables-from-view-to-html-template
        print(request.POST.get("inSemester"))
        manager = dbhelper.dbManager()
        manager.connect("root", "password12", "university") #poor form to keep in code
        feature_six_results = manager.getFeatureSix("CS", 1)
        for (courseID, sectionID) in feature_six_results:
            classes[courseID] = sectionID

        return render(request, 'usertype/student.html', context)

    else:
        return render(request, 'usertype/student.html', context)



# return render(request, 'usertype/student.html', context)


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
