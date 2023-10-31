from django.shortcuts import render
from . models import Contact,User
from django.conf import settings
from django.core.mail import send_mail
import random
# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=='POST':
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            mobile=request.POST['mobile'],
            remarks=request.POST['remarks'],
        )
        msg="Contact Saved Successfully"
        contacts=Contact.objects.all().order_by('-id')[:3]
        print(contacts)
        return render(request,'contact.html',{'msg':msg, 'contacts':contacts})
    else:
        contacts=Contact.objects.all().order_by('-id')
        return render(request,'contact.html',{'contacts':contacts})

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email Address Already Registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            
            if request.POST['password']==request.POST['cpassword']:
                    
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],
                    profile_pic=request.POST['profile_pic'],
                )
                msg="User Sign Up Successfully"
                return render(request,'login.html',{'msg':msg})
            
            else:
                msg="Password and confirm password does not matched"
                return render(request,'signup.html',{'msg':msg})
        
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=='POST':
        try:
            user=User.objects.get(
                email=request.POST['email'],
                password=request.POST['password']
            )
            request.session['email']=user.email
            request.session['fname']=user.fname
            request.session['profile_pic']=user.profile_pic.url
            return render(request,'index.html')
        except:
            msg="Invalid Email or Password"
            return render(request,'login.html',{'msg':msg})
    else:    
        return render(request,'login.html')
    
def logout(request):
    try:
        del request.session['email']
        del request.session['fname']

        return render(request,'login.html')
    except:
        return render(request,'login.html')
        


def change_password(request):
    if request.method=="POST":
        old_password=request.POST['old_password']
        new_password=request.POST['new_password']
        cnew_password=request.POST['cnew_password']
        user=User.objects.get(email=request.session['email'])

        if user.password==old_password:
            if new_password==cnew_password:
                user.password=cnew_password
                user.save()
                try:
                    del request.session['email']
                    del request.session['fname']
                    msg="Password changed successfully!Login Again"
                    return render(request,'login.html',{'msg':msg})
                except:
                    return render(request,'login.html')
                
            else:
                msg="New password and confirm new password does not matched!"
                return render(request,'change_password.html',{'msg':msg})
            
        else:
            msg="User password and old password does not matched!"
            return render(request,'change_password.html',{'msg':msg})
    else:   

        return render(request,'change_password.html')
    
def forgot_password(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            otp=random.randint(1000,9999)
            subject = 'OTP For Forgot Password'
            message = 'Hello'+user.fname+"OTP For Forgot Password is "+str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'otp.html',{'email':user.email,'otp':otp})
        except:
            msg="Email not registered"
            return render(request,'forgot_password.html',{'msg':msg})
    else:
        return render(request,'forgot_password.html')
    
def verify_otp(request):
    email=request.POST['email']
    otp=request.POST['otp']
    uotp=request.POST['uotp']

    if otp==uotp:
        return render(request,'new_password.html',{'email':email})
    
    else:
        msg="Incorrect OTP"
        return render(request,'otp.html',{'email':email,'otp':otp,'msg':msg})
    
def new_password(request):
    email=request.POST['email']
    np=request.POST['new_password']
    cnp=request.POST['cnew_password']

    if np==cnp:
        user=User.objects.get(email=email)
        user.password=np
        user.save()
        msg="Password Updated Successfully"
        return render(request,'login.html',{'msg':msg})
    else:
        msg="Password and Confirm Password Does Not matched"
        return render(request,'new_password.html',{'email':email,'msg':msg})
    
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.email=request.POST['email']
        user.mobile=request.POST['mobile']
        user.address=request.POST['address']
        try:
            user.profile_pic=request.FILES['profile_pic']
        except: 
            pass
        user.save()
        request.session['profile_pic']=user.profile_pic.url
        msg="Profile Updated Successfully"
        return render(request,'profile.html',{'user':user,'msg':msg})
    else:
        return render(request,'profile.html',{'user':user})
        