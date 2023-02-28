from django.urls import path
from . import views

urlpatterns = [
    path('submit/expense/', views.submit_expense, name='submit_expense'),
    path('submit/income/', views.submit_income, name='submit_income'),
    path('account/register/', views.register, name='register'),
    path('q/generalstat/', views.generalstat, name='generalstat'),
    path('', views.index, name='index'),
]