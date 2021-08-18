from account.models import ResetPassRequest
from home.models import MyUser
from django.core import exceptions
from django.db import models
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from dashboard.models import Attendance, Class, Link, Student
from datetime import  timedelta
import datetime
from django.utils import timezone
from django.contrib import messages
from json import loads


# Create your views here.


@staff_member_required
def dashboard(request):
    return redirect('/dashboard/classes/')



@staff_member_required
def links(request,  id=None):
    if(request.method == 'POST'):
        class_name = request.POST['class']
        expiry = int(request.POST['expiry'])
        time = request.POST['time'].lower()
        class_name = Class.objects.filter(name=class_name).order_by('-id')
        if(len(class_name) != 0):

            if(time == 'seconds'):
                expiry = timezone.now() + timedelta(seconds=expiry)
            elif(time == 'minutes'):
                expiry = timezone.now() + timedelta(minutes=expiry)
            elif(time == 'hours'):
                expiry = timezone.now() + timedelta(hours=expiry)
            else:
                expiry = timezone.now() + timedelta(minutes=2)
            try:
                link = Link.objects.create(class_name=class_name.first(), expiry=expiry)
                link.save()
                expiry_time = request.POST['expiry']
                messages.success(request, f"Successfully created a new link for  {expiry_time} {time}.")
                return redirect('/dashboard/links/')
            except Exception as e:
                messages.error(request, 'Faild to create new link')
                return redirect('/dashboard/links/')

        else:
            messages.error(request, 'The class you have selected is not available')
            return redirect('/dashboard/links/')





    elif(request.method == 'GET'):
        all_links = Link.objects.all().order_by('-id')
        all_classes = Class.objects.all().order_by('-id')
        context = {
            'links': all_links,
            'classes': all_classes,
            'attendance': Attendance.objects.all().order_by('-id'),
        }
        return render(request, 'dashboard/links.html', context)

@staff_member_required
def singleLink(request,  id=None):
    if(request.method == 'GET'):
        links = Link.objects.filter(id=id)
        context = {}
        if(len(links) != 0):
            link = links.first()
            students = link.class_name.students.all()
            attendance = Attendance.objects.filter(link=link).order_by('-id')
            attend_student = []
            for student in attendance:
                attend_student.append(student.student)
            attendance_p = round(len(attend_student) / len(students)  * 100)
            context = {
                'link': link,
                'attendance': attendance,
                'attendance_p': attendance_p,
                'students': students,
                'class': link.class_name,
                'attend_student': attend_student,
            }
        else:
            return HttpResponseNotFound()

        return render(request, 'dashboard/link.html', context)

    elif(request.method == 'POST'):
        studentList = request.POST.getlist('students')
        try:
            link = Link.objects.get(id=id)
        except Link.DoesNotExist:
            messages.error(request, 'Link does not exist!!')
            return redirect(request.path_info)

        for studentId in studentList:
            try:
                student = Student.objects.get(id=studentId)
            except Student.DoesNotExist:
                messages.error(request, f"Student with id {student.student.id} was not found!!.")
            try:
                attendance = Attendance.objects.create(student=student,  link=link)
                attendance.save()
                messages.success(request, f"Your attendance for {student.student.first_name} {student.id} was added successfully.")
            except Exception:
                messages.error(request, f"Your attendance for {student.student.first_name} {student.id} was not added!!.")

        return redirect(request.path_info)





@staff_member_required
def classes(request, id=None):
    if(id is not None):
        myClasses = Class.objects.filter(id=id)
        if(len(myClasses) != 0):
            myClass = myClasses.first()
            if(request.method == 'GET'):
                context = {
                    'class': myClass,
                    'students': Student.objects.all()
                }
                return render(request, 'dashboard/class.html', context)
            elif(request.method == "POST"  ):
                postType = request.POST['type']
                if(postType == 'class-delete'):
                    myClass.delete()
                    messages.success(request, 'Successfully deleted class.')
                    return redirect('/dashboard/classes/')
                elif(postType == 'student-delete'):
                    studentId = request.POST['student-id']
                    student = Student.objects.get(id=studentId)
                    myClass.students.remove(student)
                    messages.success(request, 'Successfully removed the student.')
                    return redirect('/dashboard/classes/'+ str(id))
                elif(postType == 'student-add'):
                    students = request.POST.getlist('students')
                    for student in students:
                        myClass.students.add(student)
                    myClass.save()
                    messages.success(request, 'The students were added successfully.')
                    return redirect('/dashboard/classes/'+ str(id))

        else:
            messages.error(request, 'This class is not available')
            return redirect('/dashboard/classes/')




    else:
        if(request.method == 'GET'):
            classes = Class.objects.all()
            context = {
                'classes': classes,
                'students': Student.objects.all()

            }
            return render(request, 'dashboard/classes.html', context)
        elif(request.method == 'POST'):
            class_name = request.POST['class-name']
            time = request.POST['time']
            studentsId = request.POST.getlist('students')
            myClass = Class.objects.create(name=class_name, time=time)
            for id in studentsId:
                student = Student.objects.get(id=id)
                myClass.students.add(student)
            myClass.save()
            messages.success(request, 'Class created successfully.')
            return redirect('/dashboard/classes/')



@staff_member_required
def studentRequest(request):
    if(request.method == 'GET'):
        students = MyUser.objects.filter(is_student=False, is_staff=False, in_draft=False)

        context = {
            'students':students
        }

        return render(request, 'dashboard/student-requests.html', context)
    elif(request.method == 'POST'):
        action = request.POST['action']
        id = request.POST['id']
        if(action == 'accept'):
            user = MyUser.objects.filter(id=id)
            if(len(user) != 0):
                user = user.first()
                user.is_student = True
                user.in_draft = False
                user.save()
                student = Student.objects.create(student=user)
                student.save()
                messages.success(request, 'Success fully added to student list.')
                return redirect('/dashboard/students/requests/')
            else:
                messages.error(request, 'This student request is not available..')
                return redirect('/dashboard/students/requests/')

        elif(action == 'reject'):
            user = MyUser.objects.filter(id=id)
            if(len(user) != 0):
                user = user.first()
                user.is_student = False
                user.in_draft = True
                user.save()
                messages.success(request, 'Success fully added to drafts.')
                return redirect('/dashboard/students/requests/')
            else:
                messages.error(request, 'This student request is not available..')
                return redirect('/dashboard/students/requests/')




@staff_member_required
def students(request, id=None):
    if(request.method == 'GET'):
        students = Student.objects.all()
        studentList = []
        for student in students:
            if(student.student in MyUser.objects.filter(is_active=True, is_student=True, in_draft=False)):
                studentList.append(student)
        context = {
            'students':studentList
        }

        return render(request, 'dashboard/students.html', context)
    if(request.method == 'POST'):
        action = request.POST['action']
        id = request.POST['id']
        userId = request.POST['user-id']
        user = MyUser.objects.get(id=userId)
        if(action == 'add-to-draft'):
            user.is_student = False
            user.in_draft = True
            user.save()
            student = Student.objects.get(id=id)
            student.delete()
            messages.success(request, 'Successfully Added Student to Draft.')
            return redirect('/dashboard/students')
        elif(action == 'remove'):
            user.delete()
            messages.success(request, 'Successfully Deleted Student.')
            return redirect('/dashboard/students')
        else:
            messages.success(request, 'Failed.')
            return redirect('/dashboard/students')


@staff_member_required
def studentDraft(request):
    if(request.method == 'GET'):
        students = MyUser.objects.filter(is_student=False, is_staff=False, in_draft=True)
        context = {
            'students':students
        }
        return render(request, 'dashboard/draft.html', context)
    elif(request.method == 'POST'):
        action = request.POST['action']
        id = request.POST['id']
        user = MyUser.objects.filter(id=id)
        if(len(user) != 0):
            if(action == 'add-to-students'):
                user = user.first()
                user.is_student = True
                user.in_draft = False
                user.save()
                student = Student.objects.create(student=user)
                student.save()
                messages.success(request, 'Success fully added to students.')
                return redirect('/dashboard/students/draft/')
            elif(action == 'delete'):
                user.first().delete()
                messages.success(request, 'Success fully deleted this request.')
                return redirect('/dashboard/students/draft/')
        else:
            messages.success(request, 'Success fully deleted this request.')
            return redirect('/dashboard/students/draft/')


@staff_member_required
def attendance(request):
    if request.method == 'GET':
        myFilter = None
        month = None
        class_name = None
        try:
            myFilter = request.GET['filter']
            month = request.GET['month']
            class_name = request.GET['class']
        except Exception as e:
            pass
        if(myFilter is not None and month is not None and class_name is not None and myFilter is not '' and month is not '' and class_name is not '' ):
            myClass = Class.objects.filter(name=class_name).first()
            students = myClass.students.all()
            nowTime = timezone.now()
            datetime_object = datetime.datetime.strptime(month, '%Y-%m')
            attendance_date = Attendance.objects.filter(attendance_date__month=datetime_object.month, attendance_date__year=datetime_object.year, link__class_name=myClass).order_by('attendance_date')
            attendance_students = []
            attendance_date_list = []
            for date in attendance_date:
                if(date.attendance_date not in attendance_date_list):
                    attendance_date_list.append(date.attendance_date)

            context = {
                'students':students,
                'attendance_date':attendance_date_list,
                'classes':Class.objects.all(),
                'selectedClass': class_name,
                'selectedMonth': month,
                'filtered': True,
                'myClass': myClass,
                'attendance_students': attendance_students,
            }
            return render(request, 'dashboard/attendance.html', context)
        else:
            nowTime = timezone.now()
            month = str(int(nowTime.month))
            if(len(month) != 2):
                month = '0'+month

            year = str(int(nowTime.year))
            context = {
                'classes':Class.objects.all(),
                'time': f"{year}-{month}"
            }
            return render(request, 'dashboard/attendance.html', context)



@staff_member_required
def deleteAttendance(request,  attendanceId):
    if(request.method == 'POST'):
        try:
            attendance = Attendance.objects.get(id=attendanceId)
            attendance.delete()
            messages.success(request, 'Successfully removed this attendance!!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except Exception as e:
            messages.error(request, 'This attendance is not available!!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required
def resPassReq(request):
    if(request.method == 'GET'):
        resPassReqs = ResetPassRequest.objects.all().order_by('id')

        for req in resPassReqs:
            for req2 in resPassReqs.filter(user=req.user):
                if(len(resPassReqs.filter(user=req.user)) != 1):
                    req2.delete()
                else:
                    break
        resPassReqs = ResetPassRequest.objects.all().order_by('-id')
        
                
        context = {
            'resPassReqs': resPassReqs
        }
        return render(request, 'dashboard/reset-pass-req.html', context)        
        
    elif(request.method == 'POST'):
        action = request.POST['action']
        reqId = request.POST['id']
        try:
            resPassReq = ResetPassRequest.objects.get(id=reqId)
        except ResetPassRequest.DoesNotExist:
            messages.error(request, 'This request does not exist any more')
            return redirect(request.path_info)
        if(action == 'allow'):
            new_pass = resPassReq.new_pass
            try:
                resPassReq.user.set_password(new_pass)
                resPassReq.user.save()
                resPassReq.delete()
                messages.success(request, 'Password reset successfull')
                return redirect(request.path_info)
            except Exception as e:
                messages.error(request, 'Password reset failed')
                return redirect(request.path_info)

            
    


