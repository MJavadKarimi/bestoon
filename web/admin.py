from django.contrib import admin
from .models import Expense, Income, Token

# Register your models here.

admin.site.register(Token)
admin.site.register(Expense)
admin.site.register(Income)