from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
import logging


# Create your views here.
def index(request):
    # return HttpResponse("hello!")
    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # return HttpResponse('login Success!')
            # return HttpResponseRedirect('/event_manage/')
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600)  # set cookies
            request.session['user'] = username  # set session
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


@login_required
def event_manage(request):
    username = request.session.get('user', '')
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user', '')  # get cookies
    return render(request, 'event_manage.html', {'user': username, 'events':event_list})


@login_required
def search_event(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})


@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    return render(request, 'guest_manage.html', {'user': username, 'guests': guest_list})


@login_required
def search_guest(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", '')
    guest_list = Guest.objects.filter(name__contains=search_name)
    return render(request, 'guest_manage.html', {'user': username, 'guests': guest_list})
