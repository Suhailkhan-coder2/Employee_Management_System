from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum
from .models import Employee


@login_required
def home(request):
    employees = Employee.objects.all()
    return render(request, 'home.html', {'employees': employees})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    total_employees = Employee.objects.count()
    total_salary = Employee.objects.aggregate(Sum('salary'))['salary__sum'] or 0

    context = {
        'total_employees': total_employees,
        'total_salary': total_salary
    }
    return render(request, 'dashboard.html', context)
@user_passes_test(lambda u: u.is_superuser)
def delete_employee(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect('home')

