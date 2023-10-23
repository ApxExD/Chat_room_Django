from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, CreateRoom
from .models import Room, Message
# Create your views here.


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not match')
    return render(request, 'base/login_page.html')

def userRegistration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            user = User.objects.create_user(username=username.lower(), password=password, email=email)
            user.save()
            login(request, user)
            return redirect('home')
        except:
            messages.error(request, 'Something went wrong. Try another username!')
    return render(request, 'base/registration_page.html')

def logoutUser(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
def home(request):

    rooms = Room.objects.all()

    context = {'rooms': rooms}

    return render(request, 'base/home.html', context)

@login_required(login_url='login_page')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_message = room.message_set.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_message': room_message}

    return render(request, 'base/room.html', context)

@login_required(login_url='login_page')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    room_id = message.room.id
    if request.method == 'POST':
        message.delete()
        return redirect(f'/room/{room_id}')
    return render(request, 'base/delete_message.html', {'obj':message})

@login_required(login_url='login_page')
def createRoom(request):
    form = CreateRoom
    if request.method == 'POST':
        room_name = request.POST.get('name')

        Room.objects.create(
           host=request.user,
           name=room_name,
       )
        return redirect('home')
    context = {'form': form}
    return render(request, 'base/create_room.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Only host can delete this room.')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html',{'obj':room})



