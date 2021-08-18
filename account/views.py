from account.models import ResetPassRequest
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from home.models import MyUser

# Create your views here.
    
def loginUser(request):
    if(request.user.is_authenticated):
        return HttpResponseNotFound()
    else:
        if(request.method == "GET"):
          
            return render(request, 'account/login.html')

        if(request.method == 'POST'):
            email = request.POST['email']
            password = request.POST['password']
            try:
                authUser = authenticate(request, email=email, password=password)
                if(authUser is not None):
                    login(request, authUser)
                    messages.success(request, 'Successfully logged in!!')
                    return redirect('/')
                else:
                    messages.error(request, 'Failed to login!! Email or password does not match. Please try again')
                    return redirect('/accounts/login/')
            except Exception as e:
                messages.error(request, 'Failed to Login!! Some error occured.')
                return redirect('/accounts/login/')
                    
        else:
            return HttpResponseNotFound()
                    

def logoutUser(request):
    if(request.method == 'POST'):
        logout(request)           
        return redirect('/accounts/login/')
    else:
        return HttpResponseNotFound()

def signup(request):
    if(request.user.is_authenticated):
        return HttpResponseNotFound()
    else:
        if(request.method == "GET"):
            return render(request, 'account/signup.html')
            
        elif(request.method == "POST"):
            email = request.POST['email']
            password = request.POST['password']
            cPassword = request.POST['cpassword']
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            age = request.POST['age']
            number = request.POST['number']
            addtional_number = request.POST['add-number']
            # validating
            if(cPassword != password):
                messages.error(request, 'Password and Confirm Password Does Not Matach !! Please Try Again')
                return redirect('/accounts/signup/')
            if(len(password) < 4):
                messages.error(request, 'Password Must Be At Least 4 Charecter4 !! Please Try Again')
                return redirect('/accounts/signup/') 
            users = MyUser.objects.filter(email=email)
            if(len(users) == 0):
                try:
                    user = MyUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, age=age, number=number, addtional_number=addtional_number)
                    user.save()
                    try:
                        authUser = authenticate(request, email=email, password=password)
                        if(authUser is not None):
                            login(request, authUser)
                            messages.success(request, 'Successfully created an account and logged in!!')
                            return redirect('/')
                        else:
                            messages.error(request, 'Successfully created an account But Failed to login!!')
                            return redirect('/accounts/login/')
                    except Exception as e:
                        messages.error(request, 'Successfully created an account But Failed to Login !!')
                        return redirect('/accounts/login/')
                            

                except Exception as e:
                    messages.error(request, 'Faild to signup !! Please Try Again')
                    return redirect('/accounts/signup/') 
            else:
                messages.error(request, 'This email address is already in use !! Try with an other email address ')
                return redirect('/accounts/login/')
        

        else:
            return HttpResponseNotFound()
        
def resetPass(request):
    if(not request.user.is_authenticated):
        if(request.method == 'GET'):
            return render(request, 'account/reset-pass.html')
        elif(request.method == 'POST'):
            email = request.POST['email']
            password = request.POST['password']
            cpassword = request.POST['cpassword']
            if(password == cpassword):
                try:
                    user = MyUser.objects.get(email=email)
                except MyUser.DoesNotExist:
                    messages.error(request, 'Email does not exist!!')
                    return redirect('/accounts/reset-password/')
                resPassReq = ResetPassRequest.objects.create(user=user, new_pass=password)
                try:
                    resPassReq.save()
                    messages.success(request, 'Your request for reset password has been submited succesfully!!')
                    return redirect('/accounts/login/')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Some Error Ocurred!!')
                    return redirect('/accounts/reset-password/')
                
            else:
                messages.error(request, 'Make sure password and confirm passwords are same!!')
                return redirect('/accounts/reset-password/')
    else:
        return redirect('/')

                
                