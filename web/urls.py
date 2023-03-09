from django.urls import path
from . import views

urlpatterns = [
    path('submit/expense/', views.submit_expense, name='submit_expense'),
    path('edit/expense/', views.edit_expense, name='edit_expense'),
    path('submit/income/', views.submit_income, name='submit_income'),
    path('edit/income/', views.edit_income, name='edit_income'),
    path('q/generalstat/', views.generalstat, name='generalstat'),
    path('q/expenses/', views.query_expenses, name='query_expenses'),
    path('q/incomes/', views.query_incomes, name='query_incomes'),
    path('q/generalstat/', views.generalstat, name='generalstat'),
    path('account/register/', views.register, name='register'),
    path('account/login/', views.login, name='login'),
    path('', views.index, name='index'),
]