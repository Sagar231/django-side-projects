from django.shortcuts import render,redirect
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm,UserLoginForm,UserRegistrationForm
from .models import Expense
import datetime

# Create your views here.

@login_required
def index(request):
    user = request.user
    
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.user = user
            expense.save()
        return redirect('index')
    
    expenses = Expense.objects.filter(user=user)
    total_expenses = expenses.aggregate(Sum('amount'))

    # Logic to calculate 365 days expenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    yearly_data = expenses.filter(date__gt=last_year)
    yearly_sum = yearly_data.aggregate(Sum('amount'))

    # Last 30 days
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    monthly_data = expenses.filter(date__gt=last_month)
    monthly_sum = monthly_data.aggregate(Sum('amount'))

    # Last week
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    weekly_data = expenses.filter(date__gt=last_week)
    weekly_sum = weekly_data.aggregate(Sum('amount'))

    # Daily sums for the last month
    daily_sums = (
        monthly_data
        .annotate(truncated_date=TruncDate('date'))
        .values('truncated_date')
        .annotate(sum=Sum('amount'))
        .order_by('truncated_date')
    )

    # Categorical sums
    categorical_sums = expenses.values('category').order_by('category').annotate(sum=Sum('amount'))

    expense_form = ExpenseForm()

    return render(request, 'myapp/index.html', {
        'expense_form': expense_form,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'yearly_sum': yearly_sum,
        'monthly_sum': monthly_sum,
        'weekly_sum': weekly_sum,
        'daily_sums': daily_sums,
        'categorical_sums': categorical_sums
    })


@login_required
def edit(request,id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    if request.method == 'POST':
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
        return redirect('index')

    return render(request,'myapp/edit.html',{'expense_form':expense_form})

@login_required
def delete(request,id):
    if request.method == "POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')

def user_login(request):
    if request.method =="POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username = data['username'],
                                password = data['password']
                                )
            if user:
                login(request,user)
                return redirect('index')
            else:
                return render(request,'myapp/wronglogin.html')
    login_form = UserLoginForm()
    return render(request,"myapp/login.html",{"form":login_form})

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method =='POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('index')
    else:
        user_form = UserRegistrationForm()

    return render(request,'myapp/register.html',{'user_form':user_form})



#######
# old code when we desplayed all the data all together without thinking about the user
######


# @login_required
# def index(request):
#     if request.method=='POST':
#         expense = ExpenseForm(request.POST)
#         if expense.is_valid():
#             expense.save()
#         return redirect('index')
#     expenses  = Expense.objects.all()
#     total_expenses = expenses.aggregate(Sum('amount'))

#     #logic to calculate 365 days expenses
#     last_year = datetime.date.today()-datetime.timedelta(days=365)
#     data = Expense.objects.filter(date__gt = last_year)
#     yearly_sum = data.aggregate(Sum('amount'))

#     #last 30 days
#     last_month = datetime.date.today()-datetime.timedelta(days=30)
#     data = Expense.objects.filter(date__gt = last_month)
#     monthly_sum = data.aggregate(Sum('amount'))

#     #last week
#     last_week = datetime.date.today()-datetime.timedelta(days=7)
#     data = Expense.objects.filter(date__gt = last_week)
#     weekly_sum = data.aggregate(Sum('amount'))

#     #code in the lecture
#     # daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))


#     #my_code
#     daily_sums = (
#                     Expense.objects.filter(date__gt=last_month)
#                     .annotate(truncated_date=TruncDate('date'))
#                     .values('truncated_date')
#                     .annotate(sum=Sum('amount'))
#                     .order_by('truncated_date')
#                 )   
#     categoricl_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    

#     expense_form = ExpenseForm()

#     return render(request,'myapp/index.html',
#                   {
#                       'expense_form':expense_form,
#                       'expenses':expenses,
#                       'total_expenses':total_expenses,
#                       'yearly_sum':yearly_sum,
#                       "monthly_sum":monthly_sum,
#                       "weekly_sum":weekly_sum,
#                       "daily_sums":daily_sums,
#                       "categorical_sums":categoricl_sums
#                       })