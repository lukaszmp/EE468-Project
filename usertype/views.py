from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from . import dbhelper
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

#TODO: connect to dtp and pass helper insatce to this file, stop opening every time a button is pressed!

def admin(request):
	if request.user.groups.all()[0].name == 'Admin':
		classes = {}
		context = {'list': classes}
		if (request.method == 'POST'): #https://www.etutorialspoint.com/index.php/257-django-pass-variables-from-view-to-html-template
			sortBY = request.POST.get("inSort")
			prof = request.POST.get("inProfessor")
			semester = request.POST.get("inSemester")
			featNum = request.POST.get("featNum")  # should be turned to a radio button

			print(semester)

			if (featNum == ""):
				print("Empty")  # be careful this wont do anything if not filled in
				return render(request, 'usertype/admin.html', context)


			# featNum = int(featNum)
			if (featNum == "1"):
				byName = False
				byDept = False
				bySalary = False

				if (sortBY == "1"):
					byName = True
				elif (sortBY == "2"):
					byDept = True
				elif (sortBY == "3"):
					bySalary = True

				manager = dbhelper.dbManager()
				manager.connect("root", "1234", "university")  # poor form to keep in code
				feature_one_results = manager.getFeatureOne(inByName=byName, inByDept=byDept, inBySalary=bySalary)
				i = 0
				for (name) in feature_one_results:
					classes[i] = name
					i = i + 1

			elif (featNum == "2"):
				manager = dbhelper.dbManager()
				manager.connect("root", "1234", "university")  # poor form to keep in code
				feature_two_results = manager.getFeatureTwo()
				i = 1
				inName = "Name"
				inMin = "Min"
				inMax = "Max"
				inAvg = "Avg"
				classes[0] = {inName, inMin, inMax, inAvg}
				for (name, min, max, avg) in feature_two_results:
					classes[i] = (name + ":" + str(min) + ":" + str(max) + ":" + str(avg))
					classes[i] = classes[i].split(":")
					i = i + 1

			elif (featNum == "3"):
				manager = dbhelper.dbManager()
				manager.connect("root", "1234", "university")  # poor form to keep in code
				feature_three_results = manager.getFeatureThree(prof, semester)
				i = 1
				classes[0] = {"Name",
							  "Department",
							  "# Students"}
				for (name, deptName, count) in feature_three_results:
					classes[i] = (name + ":" + deptName + ":" + str(count))
					classes[i] = classes[i].split(":")
					i = i + 1

			else:
				return render(request, 'usertype/admin.html', context)


			return render(request, 'usertype/admin.html', context)

		else:
			return render(request, 'usertype/admin.html', context)
	else:
		return HttpResponse('Access Denied')

# def professor(request):
#     classes = {}
    # context = {'list': classes}

def professor(request):
	if (request.user.groups.all()[0].name == 'Professor') or (request.user.groups.all()[0].name == 'Admin'):
		classes = {}
		context = {'list': classes}
		if (request.method == 'POST'): #https://www.etutorialspoint.com/index.php/257-django-pass-variables-from-view-to-html-template
			prof = request.POST.get("inProfessor")
			semester = request.POST.get("inSemester")
			featNum = request.POST.get("featNum")

			if (featNum == "4"):
				manager = dbhelper.dbManager()
				manager.connect("root", "1234", "university")  # poor form to keep in code
				feature_four_results = manager.getFeatureFour(prof, semester)

				i = 1
				classes[0] = {"Name",
							  "Course",
							  "Section",
							  "Count"}
				for (name, course, section, count) in feature_four_results:
					classes[i] = (name + ":" + course + ":" + section + ":" + str(count)) #split string in js side for better display
					classes[i] = classes[i].split(":")
					i = i + 1

				print(semester)

				return render(request, 'usertype/professor.html', context)

			elif (featNum == "5"):
				manager = dbhelper.dbManager()
				manager.connect("root", "1234", "university") #poor form to keep in code
				feature_five_results = manager.getFeatureFive(prof, semester)

				i = 1
				classes[0] = {"Students"}
				for (studentName) in feature_five_results:
					classes[i] = studentName
					i = i + 1

				return render(request, 'usertype/professor.html', context)
			else:
				return render(request, 'usertype/professor.html', context) #never return None

		else:
			return render(request, 'usertype/professor.html', context)


		return render(request, 'usertype/professor.html', context)
	else:
		return HttpResponse('Access Denied')


def student(request):
	if (request.user.groups.all()[0].name == 'Student'):
		classes = {}
		context = {'list': classes}
		if (request.method == 'POST'): #https://www.etutorialspoint.com/index.php/257-django-pass-variables-from-view-to-html-template
			dept = request.POST.get("inDepartment")
			semester = request.POST.get("inSemester")
			manager = dbhelper.dbManager()
			manager.connect("root", "1234", "university") #poor form to keep in code
			feature_six_results = manager.getFeatureSix(dept, semester)
			for (courseID, sectionID) in feature_six_results:
				classes[courseID] = sectionID

			print(semester)

			return render(request, 'usertype/student.html', context)

		else:
			return render(request, 'usertype/student.html', context)
	else:
		return HttpResponse('Access Denied')



# return render(request, 'usertype/student.html', context)


def user_login(request):
	#creating some dummy users for testing
    if not (User.objects.filter(username='admin').exists()):
        admin_object = User.objects.create_user(username='admin', password='EE468CS460')
        professor_object = User.objects.create_user(username='professor', password='EE468CS460')
        student_object = User.objects.create_user(username='student', password='EE468CS460')
		
        admin_group = Group.objects.get_or_create(name="Admin")
        professor_group = Group.objects.get_or_create(name="Professor")
        student_group = Group.objects.get_or_create(name="Student")
		
        admin_group.user_set.add(admin_object)
        professor_group.user_set.add(professor_object)
        student_group.user_set.add(student_object)
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
