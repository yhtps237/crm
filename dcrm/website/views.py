from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.

def home(request):
    records = Record.objects.all()

    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
        else:
            messages.success(request, "There was an error logging in, Please Try Again.")
        return redirect('home')
    return render(request, 'home.html', {"records": records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered.")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    
    messages.success(request, "You must be logged in to view that page.")
    return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added.")
                return redirect('home')
            
        return render(request, 'add_record.html', {'form': form})
    
    messages.success(request, "You must be logged in to view that page.")
    return redirect('home')
    

def customer_record_update(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=customer_record)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Record updated.")
                return redirect('home')
            

        return render(request, 'update_record.html', {'form': form})
    
    messages.success(request, "You must be logged in to view that page.")
    return redirect('home')


def customer_record_delete(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        customer_record.delete()
        messages.success(request, "Record deleted successfully.")
        return redirect('home')
    
    messages.success(request, "You must be logged in to view that page.")
    return redirect('home')
