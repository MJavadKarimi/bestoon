from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import User, Token, Expense, Income
from datetime import datetime

# Create your views here.

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
