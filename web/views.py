from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import User, Token, Expense, Income, Passwordresetcodes
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from captcha.fields import ReCaptchaField
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum, Count


# Create your views here.

# homepage of System

def index(request):
    context = {}
    return render(request, 'index.html', context)


def grecaptcha_verify(request):
    # api
    pass


def register(request):
    if 'requestcode' in request.POST: # form is filled. if not spam, generate code and save in db. wait for email confirmation, return message.
        
        # is this spam? check reCaptcha.
        captcha = ReCaptchaField(request.POST)
        if not captcha: # captcha was not correct
            context = {
                'message': 'کپچای گوگل درست وارد نشده است. لطفا با به درستی وارد کنید!'} # TODO: forget password
            return render(request, 'register.html', context)

        # duplicate email
        if User.objects.filter(email=request.POST['email']).exists():
            context = {
                'message': '.این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شماست، گزینه فراموشی پسورد رو انتخاب کنین'}
            return render(request, 'register.html', context) # TODO: forget password # TODO: keep the form data
        
        # if user does not exists
        if not User.objects.filter(username=request.POST['username']).exists():
            code = get_random_string(length=32)
            now = datetime.now()
            email = request.POST['email']
            username = request.POST['username']
            password = make_password(request.POST['password'])
            temporarycode = Passwordresetcodes.objects.create(code=code ,email=email ,time=now ,username=username , password=password )

            # message = PMMail(api_key=settings.POSTMARK_API_TOKEN,
            #                 subject="فعالسازی اکانت بستون",
            #                 sender="jadi@jadi.net",
            #                 to=email,
            #                 text_body=" برای فعال کردن اکانت بستون خود روی لینک روبرو کلیک کنید: {}?code={}".format(
            #                     request.build_absolute_uri('/accounts/register/'), code),
            #                 tag="account request")
            # message.send()
            # message = 'ایمیلی حاوی لینک فعال سازی اکانت به شما فرستاده شده، لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'
            
            message = 'قدیم ها ایمیل فعال سازی می فرستادیم ولی الان شرکتش ما رو تحریم کرده (: پس راحت و بی دردسر'
            body = " برای فعال کردن اکانت بستون خود روی لینک روبرو کلیک کنید: <a href=\"{}?code={}\">لینک رو به رو</a> "\
                .format(request.build_absolute_uri('/accounts/register/'), code)
            message = message + body
            context = {
                'message': message }
            return render(request, 'index.html', context)
        else:
            context = {
                'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید.'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'register.html', context)

    elif 'code' in request.GET: # user clicked on code (link)
        code = request.GET['code']
        if Passwordresetcodes.objects.filter(code=code).exists(): # if code is in temporary db, read the data and create the user
            new_tmp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password, email=new_temp_user.email)
            this_token = get_random_string(length=48)
            token = Token.objects.create(user=newuser, token=this_token)
            # delete the temporary activation code from db
            Passwordresetcodes.objects.filter(code=code).delete()
            context = {
                'message': 'اکانت شما ساخته شد. توکن شما {} است. آن را ذخیره کنید چون دیگر نمایش داده نخواهد شد! جدی!'.format(
                    this_token)}
            return render(request, 'index.html', context)
        else:
            context = {
                'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'register.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)


@csrf_exempt
def generalstat(request):
    # TODO: should get a valid duration (from - to), if not, use 1 mounth
    # TODO: is the token valid?
    this_token = request.POST['token']
    this_user = get_object_or_404(User, token__token=this_token)
    income = Income.objects.filter(user=this_user).aggregate(Count('amount'), Sum('amount'))
    expense = Expense.objects.filter(user=this_user).aggregate(Count('amount'), Sum('amount'))
    context = {}
    context['expense'] = expense
    context['income'] = income
    # return {'income':'INCOME','expanse':'EXPANSE'}
    return JsonResponse(context, encoder=JSONEncoder)


@csrf_exempt
def submit_income(request):
    """user submit an income"""

    #TODO: validate data. user might be fake. token might be fake. amount might be...
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()
    Income.objects.create(title=request.POST['title'], amount=request.POST['amount'], date=date, user=this_user)

    return JsonResponse({
        'status': 'ok'
    }, encoder=JSONEncoder)


@csrf_exempt
def submit_expense(request):
    """user submit an expense"""

    #TODO: validate data. user might be fake. token might be fake. amount might be...
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()
    Expense.objects.create(title=request.POST['title'], amount=request.POST['amount'], date=date, user=this_user)

    return JsonResponse({
        'status': 'ok'
    }, encoder=JSONEncoder)
