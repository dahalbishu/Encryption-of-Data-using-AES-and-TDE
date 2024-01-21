# myapp/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from main import enter_data,retreive_data


def view_home(request):
    return render(request, 'home.html')


def insert_data(request):
    if request.method == 'POST':
        print("jelll")
        name = request.POST.get('name')
        email = request.POST.get('email')
        creditCard = request.POST.get('creditCard')
        print(name)
        # Now you have the values from the form
        print("Name:", name)
        print("Email:", email)
        print("Credit Card:", creditCard)
        status = enter_data(name,email,creditCard)
        if (status == 0):
            color = 'red'
            var = 'Email already exists!'
        elif (status == 1):
            color = 'green'
            var = 'Info Stored Successfully!'
        # Now you have the values from the form
        print(name,email,creditCard)


        # Add your logic to save the data to the database or perform other actions
    return render(request, 'home.html', {'status':var,'color':color})


def view_data(request):

    if request.method == 'POST':
        print("jelll")
        viewemail = request.POST.get('viewemail')
        print(viewemail)
        try:
            namee, email, ccn = retreive_data(viewemail)
        except:
            namee = 'Not Found!'
            email ='Not Found!'
            ccn = 'Not Found!'

        
    return render(request, 'home.html',{'namee':namee, 'email':email, 'ccn':ccn})
