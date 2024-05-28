from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from random import randint
from django.contrib import messages


# Create your views here.
def index(request):
    testimonial = Testimonials.objects.all()
    return render(request, 'index.html',{'Testimonials':testimonial})

def about(request):
    return render(request, 'about-us.html')

def contact(request):
    return render(request, 'contact.html')

def services(request):
    testimonial = Testimonials.objects.all()
    return render(request, 'services.html',{'Testimonials':testimonial})

def testimonials(request):
    testimonial = Testimonials.objects.all()
    return render(request, 'testimonials.html',{'Testimonials':testimonial})

def careers(request):
    jobs = Jobs.objects.all()
    testimonial = Testimonials.objects.all()
    return render(request, 'pricing.html', {'Jobs':jobs,'Testimonials':testimonial})

def login(request):
    return render(request, 'login.html')

def otp(request):
    return render(request, 'otp.html')

def applications(request):
    applications = Applications.objects.all()
    return render(request, 'applications.html',{'applications':applications})

def addjobs(request):
    Job = Jobs.objects.all()
    return render(request, 'addjobs.html',{'Jobs':Job})

@csrf_exempt
@api_view(["POST"])
def contact_form(request):
    fname = request.data.get('First_Name')
    lname = request.data.get('Last_Name')
    email = request.data.get('Email')
    mobile = request.data.get('Mobile')
    comments = request.data.get('Comments')
    print(fname,'--->')
    if not fname:
        return JsonResponse({"Status":False,"Msg":"Please enter your first name!!"})
    
    if not email:
        return JsonResponse({"Status":False,"Msg":"Please enter your mail id!!"})
    
    if not mobile:
        return JsonResponse({"Status":False,"Msg":"Please enter your mobile number!!"})
    
    if len(mobile)<10 or len(mobile)>10:
        return JsonResponse({"Status":False,"Msg":"Please enter valid mobile number!!"})
    
    Contact.objects.create(
        First_Name=fname,
        Last_Name=lname,
        Email=email,
        Mobile=mobile,
        Comments=comments
    )
    return JsonResponse({"Status":True,"redirect_url":reverse('contact')})
    
@csrf_exempt
@api_view(["POST"])
def testimonial_form(request):
    fname = request.data.get('First_Name')
    lname = request.data.get('Last_Name')
    sub_feed = request.data.get('Sub_Feedback')
    feedback = request.data.get('Feedback')
    # picture = request.data.get('Picture')

    if not fname:
        return JsonResponse({"Status":False,"Msg":"Please Enter First Name!!"})
    if not lname:
        return JsonResponse({"Status":False,"Msg":"Please enter last name!!"})
    if not sub_feed:
        return JsonResponse({"Status":False,"Msg":"Please enter subject for feedback!!"})
    if not feedback:
        return JsonResponse({"Status":False,"Msg":"Please enter feedback!!"})
    
    Testimonials.objects.create(
        First_Name=fname,
        Last_Name=lname,
        Sub_Feedback=sub_feed,
        Feedback=feedback,
        # image=picture
    )
    print('Feedback saved')
    return JsonResponse({"Status":True,"redirect_url":reverse('testimonials')})

@csrf_exempt
@api_view(["POST"])
def mailform(request):
    name = request.data.get('Name')
    email = request.data.get('Email')
    subject = request.data.get('Subject')
    text = request.data.get('Text')

    if not name:
        print('name missing!!')
        return JsonResponse({"Status":False,"Msg":"Please enter your first name!!"})
    if not email:
        print('email missing!!')
        return JsonResponse({"Status":False,"Msg":"Please enter email id!!"})
    if not subject:
        print('subject missing!!')
        return JsonResponse({"Status":False,"Msg":"please  enter subject to send mail!!"})
    if not text:
        print('text missing!!')
        return JsonResponse({"Status":False,"Msg":"Please enter Your text message to send us!!"})
    
    from django.core.mail import send_mail
    send_mail(
        subject,
        f"{name}{text}",
        email,
        ['divybavishi001@gmail.com'],
        fail_silently=False
    )
    print('mail sent!!')
    return JsonResponse({"Status":True,"redirect_url":reverse('index')})

@csrf_exempt
@api_view(["POST"])
def Emp_Login(request):
    emailormobile = request.data.get('EmailorMobile')
    print(emailormobile,'-->')
    password = request.data.get('Password')

    try:
        emp = Employee.objects.get(Phone=emailormobile)
    except Employee.DoesNotExist:
        emp = Employee.objects.get(Email=emailormobile)
    except:
        return JsonResponse({"Status":False})
    
    if password != emp.Password:
        return JsonResponse({"Status":False,"Msg":"Incurrect password please retry again!!","redirect_url":reverse('login')})
    
    otp = randint(100000, 999999)
    print(otp,'---->')

    # from django.core.mail import send_mail
    # send_mail(
    #     'Your otp for login',
    #     f'Your otp for login is {otp}',
    #     'divybavishioo1@gmail.com',
    #     [emp.Email],
    #     fail_silently=False
    # )
    emp.OTP=otp
    emp.save()
    request.session['emp']=emp.emp_id
    print(emp.emp_id,'-->')
    # return redirect('otp')
    messages.success(request, "Your Otp is sent to your mail!!,Please verify it!!")
    return JsonResponse({"Status":True})

@csrf_exempt
@api_view(["POST"])
def verify_Otp(request):
    otp = request.data.get('OTP')
    print(otp,'-->')
    emp_id = request.session.get('emp')
    print(emp_id)
    try:
        emp = Employee.objects.get(emp_id=emp_id)
        print(emp.OTP,'--->')
    except Employee.DoesNotExist:
        return JsonResponse({"Status":False,"Msg":"Please Login first!!","redirect_url":reverse('login')})
    
    if otp != emp.OTP:
        return JsonResponse({"Status":False,"Msg":"Wrong OTP,Please Try again!!","Redirect_url":reverse('otp')})
    
    emp.Active=True
    emp.save()
    print(emp_id)
    messages.success(request, "Your are logged-in successfully!!")
    return JsonResponse({"Status":False,"redirect_url":reverse('index')})

def logout_emp(request):
    emp_id = request.session.get('emp')
    try:
        emp = Employee.objects.get(emp_id=emp_id)
    except Employee.DoesNotExist:
        return JsonResponse({"Status":False,"Msg":"Your session is time out!!"})
    emp.Active=False
    emp.save()
    del request.session['emp']
    return redirect('index')

@api_view(["POST"])
def post_jobs(request):
    emp_id = request.session.get('emp')
    title = request.data.get('Title')
    desc = request.data.get('Description')
    requirment = request.data.get('Requirment')
    salary = request.data.get('Salary-Range')
    location = request.data.get('Location')

    try:
        emp = Employee.objects.get(emp_id=emp_id)
    except Employee.DoesNotExist:
        return JsonResponse({"Status":False,"Msg":"Please Login first!!"})
    
    Jobs.objects.create(
        Title=title,
        Description=desc,
        Requirments=requirment,
        Salary_Range=salary,
        Location=location
    )
    return JsonResponse({"Status":True,"Msg":"Job Posted Successfully!!"})

@api_view(["POST"])
def update_job_post(request):
    emp_id = request.session.get('emp')
    job_id = request.data.get('jobid')
    title = request.data.get('Title')
    desc = request.data.get('Description')
    requirment = request.data.get('Requirment')
    salary = request.data.get('Salary-Range')
    location = request.data.get('Location')

    try:
        emp = Employee.objects.get(emp_id=emp_id)
        job = Jobs.objects.get(job_id=job_id)
    except Employee.DoesNotExist:
        return JsonResponse({"Status":False,"Msg":"Please login first!!"})
    except Jobs.DoesNotExist:
        return JsonResponse({"Status":False,"msg":"Job id not matched, Please try again!!"})
    
    job.Title=title
    job.Description=desc
    job.Requirments=requirment
    job.Salary_Range=salary
    job.Location=location
    job.save()
    return JsonResponse({"Status":True,"Msg":"Job post is updated successfully!!"})

@api_view(["POST"])
def delete_job_post(request):
    emp_id = request.session.get('emp')
    job_id = request.data.get('jobid')

    try: 
        emp = Employee.objects.get(emp_id=emp_id)
        job = Jobs.objects.get(job_id=job_id)
    except Employee.DoesNotExist:
        return JsonResponse({"Status":False,"Msg":"Please login first!!"})
    except Jobs.DoesNotExist:
        return JsonResponse({"Status":False,"Msg":"Job id not found Please try again!!"})
    
    job.delete()
    return JsonResponse({"Status":True,"Msg":"Job post deleted!!"})

@csrf_exempt
@api_view(["POST"])
def apply_job(request):
    fname = request.data.get('First_Name')
    lname = request.data.get('Last_Name')
    email = request.data.get('Email')
    mobile = request.data.get('Mobile')
    resume = request.data.get('Resume')
    job_id = request.data.get('job_id')

    if not fname:
        return JsonResponse({"Status":False,"Msg":"Please Enter your First name to apply job!!"})
    if not lname:
        return JsonResponse({"Status":False,"Msg":"Please enter Your last name to apply jobs!! "})
    if not email:
        return JsonResponse({"Status":False,"Msg":"Please enter Your email to apply job !!"})
    if not mobile:
        return JsonResponse({"Status":False,"Msg":"Please enter mobile number to apply job!!"})
    if not resume:
        return JsonResponse({"Status":False,"Msg":"Please submit your resume!!"})
    
    try:
        job = Jobs.objects.get(job_id=job_id)
    except Jobs.DoesNotExist:
        print('job not exist!')
        return JsonResponse({"Status":False,"Msg":"job id not found please retry!!"})
    
    Applications.objects.create(
        First_Name=fname,
        Last_Name=lname,
        Email=email,
        Mobile=mobile,
        Resume=resume,
        job_id=job
    )
    print('successfull!')
    return JsonResponse({"Status":True,"Msg":"You are applied successfully!!","redirect_url":reverse('careers')})

@csrf_exempt
@api_view(["POST"])
def addnewjobs(request):
    emp_id = request.session.get('emp')
    try:
        emp = Employee.objects.get(emp_id=emp_id)        
    except Employee.DoesNotExist:
        print(emp)
        return JsonResponse({"Status":False,"redirect_url":reverse('addjobs')})
    
    title = request.data.get('Title')
    requirments = request.data.get('Requirments')
    salayrange = request.data.get('SalaryRange')
    location = request.data.get('Location')
    desc = request.data.get('Description')

    Jobs.objects.create(
        Title=title,
        Description=desc,
        Requirments=requirments,
        Salary_Range=salayrange,
        Location=location
    )
    print('created job')
    return JsonResponse({"Status":True,"redirect_url":reverse('addjobs')})
    

@csrf_exempt
@api_view(["POST"])
def editjobs(request):
    emp_id = request.session.get('emp')
    try:
        emp = Employee.objects.get(emp_id=emp_id)
    except Employee.DoesNotExist:
        print('login first!!')
        messages.error(request, "You have to login first as employee!!")
        return JsonResponse({"Status":False,"redirect_url":reverse('login')})
    
    job_id = request.data.get('Job_id')
    title = request.data.get('Title')
    requirments = request.data.get('Requirments')
    salaryrange = request.data.get('SalaryRange')
    location = request.data.get('Location')
    desc = request.data.get('Description')

    try:
        job = Jobs.objects.get(job_id=job_id)
    except Jobs.DoesNotExist:
        print('job id is not found')
        messages.error(request, "Your job id is not found!!, please try again!!")
        return JsonResponse({"Status":False,"redirect_url":reverse('addjobs')})
    
    job.Title=title
    job.Description=desc
    job.Requirments=requirments
    job.Salary_Range=salaryrange
    job.Location=location
    job.save()
    print('job updated!')
    messages.success(request, "job is updated successfully!!")
    return JsonResponse({"Status":True,"redirect_url":reverse('addjobs')})

@csrf_exempt
@api_view(["POST"])
def deletejob(request):
    job_id = request.data.get('Job_id')
    print(job_id)
    emp_id = request.session.get('emp')
    try:
        emp = Employee.objects.get(emp_id=emp_id)
        job = Jobs.objects.get(job_id=job_id)
    except Employee.DoesNotExist:
        print('employe login not found!!')
        return JsonResponse({"Status":False,"redirect_url":reverse('addjobs')})
    except Jobs.DoesNotExist:
        print('Job id not found!!')
        return JsonResponse({"Status":False,"redirect_url":reverse('addjobs')})
    
    job.delete()
    print('job deleted!!')
    return JsonResponse({"Status":True,"redirect_url":reverse('addjobs')})
    