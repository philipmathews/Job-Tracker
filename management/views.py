from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

from django.contrib.auth import login, authenticate,logout,update_session_auth_hash

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.urls import reverse

from django.forms import formset_factory,BaseFormSet

from django.contrib import messages

from django.conf import settings

from django.template.loader import render_to_string

from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_activation_token

from django.core.mail import EmailMessage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime

from .forms import UserLoginForm,SignupForm,WishListForm,AppliedForm,JobInfoForm,TaskForm

from .models import Wishlist,Applied,Task

import requests


def home(request):
    if request.user.is_authenticated:
        return redirect('management:dashboard')
    
    return render(request, 'management/home.html')

def log_in(request):
    if request.user.is_authenticated:
        return redirect('management:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('management:dashboard')
            else:
                return render(request,'management/login.html',{'form' : form,'user' : user})
    else:
        form = UserLoginForm
    context = { 'form' : form }
    return render(request,'management/login.html', context)


def log_out(request):
    logout(request)
    return redirect('management:home')


def register(request):
    if request.user.is_authenticated:
        return redirect('management:dashboard')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()

            if result['success']:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('management/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token':account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponse('An activation Link has been sent to your email address.Please Check your Inbox')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    else:
        form = SignupForm()

    context = { 'form' : form }
    return render(request, 'management/register.html', context)


def activate(request, uidb64, token,backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Thank you for your email confirmation. Now you have logged In')
        return redirect('management:dashboard')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('management:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'management/change_password.html', {'form': form})

@login_required(login_url='/login')
def dashboard(request):
    username = request.user
    wishlists = Wishlist.objects.filter(username=username)
    appliedlists = Applied.objects.filter(username=username)
    context = {
        'wishlists': wishlists,
        'appliedlists': appliedlists,
    }
    return render(request, 'management/dashboard.html',context)

@login_required(login_url='/login')
def createwishlist(request):
    if request.method == 'POST':
        wishform = WishListForm(request.POST)
        if wishform.is_valid():
            username = request.user
            wishlist = username.wishlist_set.create(company=request.POST['company'],job_title=request.POST['job_title'])
            return redirect('management:dashboard')
    else:
        wishform = WishListForm()
    context = { 'wishform' : wishform }
    return render(request,'management/createwishlist.html', context)

@login_required(login_url='/login')
def deletewishlist(request,wishlist_id):
    wishlist = get_object_or_404(Wishlist,pk=wishlist_id)
    wishlist.delete()
    return redirect('management:dashboard')

@login_required(login_url='/login')
def createapplied(request):
    if request.method == 'POST':
        appliedform = AppliedForm(request.POST)
        if appliedform.is_valid():
            username = request.user
            applied = username.applied_set.create(company=request.POST['company'],job_title=request.POST['job_title'],applied=request.POST['applied'])
            return redirect('management:dashboard')
    else:
        appliedform = AppliedForm()
    context = { 'appliedform' : appliedform }
    return render(request,'management/createapplied.html', context)

@login_required(login_url='/login')
def deleteapplied(request,applied_id):
    applied = get_object_or_404(Applied,pk=applied_id)
    applied.delete()
    return redirect('management:dashboard')

@login_required(login_url='/login')
def wishlistinfo(request,wishlist_id):
    if request.method == 'POST':
        form1 = JobInfoForm(request.POST)
        if form1.is_valid():
            wishlist_jobinfo = get_object_or_404(Wishlist,pk=wishlist_id)
            wishlist_jobinfo.company = request.POST['company']
            wishlist_jobinfo.job_title = request.POST['job_title']
            if(request.POST['deadline'] == ''):
                wishlist_jobinfo.deadline = None
            else:
                wishlist_jobinfo.deadline = request.POST['deadline']
            if(request.POST['applied'] == ''):
                wishlist_jobinfo.applied = None
            else:
                wishlist_jobinfo.applied = request.POST['applied']
            wishlist_jobinfo.location = request.POST['location']
            if(request.POST['salary'] == ''):
                wishlist_jobinfo.salary = None
            else:
                wishlist_jobinfo.salary = request.POST['salary']
            wishlist_jobinfo.post_url = request.POST['post_url']
            wishlist_jobinfo.status= request.POST['status']
            if(request.POST['offer'] == ''):
                wishlist_jobinfo.offer = None
            else:
                wishlist_jobinfo.offer = request.POST['offer']
            wishlist_jobinfo.save()
            return redirect('management:dashboard')
    else:
        wishlist_jobinfo = get_object_or_404(Wishlist,pk=wishlist_id)
        data={
            'company' : wishlist_jobinfo.company,
            'job_title' : wishlist_jobinfo.job_title,
            'deadline' : wishlist_jobinfo.deadline,
            'applied' : wishlist_jobinfo.applied,
            'location' : wishlist_jobinfo.location,
            'salary' : wishlist_jobinfo.salary,
            'post_url' : wishlist_jobinfo.post_url,
            'status' : wishlist_jobinfo.status,
            'offer' : wishlist_jobinfo.offer,
        }
        form1 = JobInfoForm(data)
    context = { 'form1' : form1 , 'wishlist_jobinfo' : wishlist_jobinfo}
    return render(request,'management/wishlistjobinfo.html',context)

@login_required(login_url='/login')
def appliedinfo(request,applied_id):
    if request.method == 'POST':
        form2 = JobInfoForm(request.POST)
        if form2.is_valid():
            applied_jobinfo = get_object_or_404(Applied,pk=applied_id)
            applied_jobinfo.company = request.POST['company']
            applied_jobinfo.job_title = request.POST['job_title']
            if(request.POST['deadline'] == ''):
                applied_jobinfo.deadline = None
            else:
                applied_jobinfo.deadline = request.POST['deadline']
            if(request.POST['applied'] == ''):
                applied_jobinfo.applied = None
            else:
                applied_jobinfo.applied = request.POST['applied']
            applied_jobinfo.location = request.POST['location']
            if(request.POST['salary'] == ''):
                applied_jobinfo.salary = None
            else:
                applied_jobinfo.salary = request.POST['salary']
            applied_jobinfo.post_url = request.POST['post_url']
            applied_jobinfo.status= request.POST['status']
            if(request.POST['offer'] == ''):
                applied_jobinfo.offer = None
            else:
                applied_jobinfo.offer = request.POST['offer']
            applied_jobinfo.save()
            return redirect('management:dashboard')
    else:
        applied_jobinfo = get_object_or_404(Applied,pk=applied_id)
        data={
            'company' : applied_jobinfo.company,
            'job_title' : applied_jobinfo.job_title,
            'deadline' : applied_jobinfo.deadline,
            'applied' : applied_jobinfo.applied,
            'location' : applied_jobinfo.location,
            'salary' : applied_jobinfo.salary,
            'post_url' : applied_jobinfo.post_url,
            'status' : applied_jobinfo.status,
            'offer' : applied_jobinfo.offer,
        }
        form2 = JobInfoForm(data)
    context = { 'form2' : form2 , 'applied_jobinfo' : applied_jobinfo}
    return render(request,'management/appliedjobinfo.html',context)

def tasks(request):
    username=request.user
    tasks = Task.objects.filter(username=username)
    context = {
        'tasks': tasks,
    }
    return render(request, 'management/tasks.html',context)

def createtask(request):
    if request.method == 'POST':
        taskform = TaskForm(request.POST)
        if taskform.is_valid():
            username = request.user
            task = username.task_set.create(title=request.POST['title'],text=request.POST['text'],date=request.POST['date'])
            return redirect('management:tasks')
    else:
        taskform = TaskForm()
    context = { 'taskform' : taskform }
    return render(request,'management/createtask.html', context)

def completetask(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.complete = True
    task.save()
    return redirect('management:tasks')

def deletecompleted(request):
    Task.objects.filter(complete__exact=True).delete()
    return redirect('management:tasks')

def deletetask(request,task_id):
    task = get_object_or_404(Task,pk=task_id)
    task.delete()
    return redirect('management:tasks')


def jobactivity(request):
    return render(request,'management/jobactivity.html')

def chartdata(request):
    dates=[]
    count=[]
    username = request.user
    wishlists_count = Wishlist.objects.filter(username=username).count()
    appliedlists_count = Applied.objects.filter(username=username).count()
    interviewed_acount = username.applied_set.filter(status__icontains='Interview').count()
    rejected_acount = username.applied_set.filter(status__icontains='Rejected').count()
    offer_acount = username.applied_set.filter(status__icontains='offer').count()
    interviewed_wcount = username.wishlist_set.filter(status__icontains='Interview').count()
    rejected_wcount = username.wishlist_set.filter(status__icontains='Rejected').count()
    offer_wcount = username.wishlist_set.filter(status__icontains='offer').count()
    interviewed_count = interviewed_acount + interviewed_wcount
    rejected_count = rejected_acount + rejected_wcount
    offer_count = offer_acount + offer_wcount
    appliedlist = username.applied_set.all()
    ordappliedlist = appliedlist.order_by('id')
    datelist = set(ordappliedlist.values_list('applied',flat=True))
    dates= sorted(list(datelist))
    print(dates)
    for date in dates:
        job_count = username.applied_set.filter(applied=date).count()
        count.append(job_count)
    labels = ["Wishlist","Applied","Interview","Rejected","Offered"]
    default_items = [wishlists_count,appliedlists_count,interviewed_count,rejected_count,offer_count]
    labels2 = dates
    default2 = count
    data={
        "labels" : labels,
        "default" : default_items,
        "labels2" : labels2,
        "default2" : default2,
    }
    return JsonResponse(data)












