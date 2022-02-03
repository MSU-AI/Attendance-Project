from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello! Welcome to the Attendence Project website. Check out the <a href='/admin'>admin panel</a> and sign in with username 'test' and password 'test'. Or view the <a href='./app'>app frontend</a>.")


def app(request):
    return render(request, "attendance-app.html")
