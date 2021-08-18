import datetime
from django.utils import timezone
from dashboard.models import Attendance, Link, Student
from home.models import MyUser
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.



@login_required
def profile(request, id=None):
    if(request.user.is_staff):
        return  redirect('/dashboard')
    else:
        if(request.method == 'GET'):
            user = request.user
            context = {
                'email': user.email,
                'fName': user.first_name,
                'lName': user.last_name,
                'age': user.age,
                'number': user.number,
                'addNumber': user.addtional_number,
            }
            return render(request, 'home/profile.html', context)
    
@login_required
def editProfile(request):
    if(request.user.is_staff):
        return redirect('/dashboard')
    else:
        if(request.method == 'GET'):
            user = request.user
            context = {
                'email': user.email,
                'fName': user.first_name,
                'lName': user.last_name,
                'age': user.age,
                'number': user.number,
                'addNumber': user.addtional_number,
            }
            return render(request, 'home/edit-profile.html', context)

        elif(request.method == 'POST'):
            request.user.email = request.POST['email']
            request.user.first_name = request.POST['first-name']
            request.user.last_name = request.POST['last-name']
            request.user.age = request.POST['age']
            request.user.number = request.POST['number']
            request.user.addtional_number = request.POST['add-number']
            request.user.save()
            return redirect('/profile/edit/')

@login_required
def attendance(request, token=None):
    if(not request.user.is_staff):
        links = Link.objects.filter(token=token)
        if(len(links) != 0):
            link = links.first()
            student = None
            try:
                student = Student.objects.get(student=request.user)
            except Exception as e:
                messages.error(request, f"You are not a verified student")
                return redirect('/')
            
            if(student not in links[0].class_name.students.all()):
                messages.error(request, f"You are not a member of this class. PLease tell your teacher to add you in the class.")
                return redirect('/')
                    

            attendance = Attendance.objects.filter(link=link, student=student)
            if(len(attendance) == 0):
                if((link.expiry - timezone.now()).total_seconds() > 0):
                    attendance = Attendance.objects.create(student=student,  link=link)
                    attendance.save()
                    messages.success(request, f"Your attendance  for {link.class_name.name} has been added successfully.")
                    return render(request, "home/attendance.html")
                else:
                    messages.error(request, f"This link for {link.class_name.name} has been expired.")
                    return render(request, "home/attendance.html")
            else:
                messages.warning(request, f'Your attendance for for {link.class_name.name} has already been added..')
                return render(request, "home/attendance.html")
        else:
            messages.warning(request, 'This link is not valid.')
            return render(request, "home/attendance.html")
    else:
        return redirect('/dashboard/links/')
    

@login_required
def myAttendance(request):
    return HttpResponse("myAttendance")