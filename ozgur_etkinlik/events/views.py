from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, HttpResponseRedirect, reverse
from .models import Event, EventMember
from .forms import EventForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'index.html')


def events(request):
    event = Event.objects.all()
    return render(request, 'events.html', {'event': event})


def detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'detail.html', {'event': event})


@login_required(login_url='/user/login/')
def profile(request):
    user = Event.objects.filter(author=request.user)
    context = {
        "user": user
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/user/login/')
def addevent(request):
    if request.method == "POST":
        form = EventForm(request.POST or None)

        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = EventForm()

    return render(request, 'addevent.html', {'form': form})


@login_required(login_url='/user/login/')
def updateEvent(request, slug):
    event = get_object_or_404(Event, slug=slug)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        event = form.save(commit=False)
        event.author = request.user
        event.save()
        return redirect('profile')

    return render(request, 'update.html', {'form': form})


@login_required(login_url='/user/login/')
def deleteEvent(request, slug):
    event = get_object_or_404(Event, slug=slug)
    event.delete()
    return redirect('profile')


@login_required(login_url='/user/login/')
def registerEvent(request, slug):
    event = get_object_or_404(Event, slug=slug)
    event_member = EventMember.objects.filter(event=event, user=request.user)
    if not event_member.exists():
        EventMember.objects.create(event=event, user=request.user)
    return redirect('index')
