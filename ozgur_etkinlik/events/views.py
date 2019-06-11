from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, Http404
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Event, EventMember, NewComment
from .forms import EventForm, CommentForm
from django.contrib import messages
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from .forms import SearchForm

from django.urls import reverse_lazy


# Create your views here.

def index(request):
    return render(request, 'index.html')


def event_list(request):
    form = SearchForm(data=request.GET or None)
    events = Event.objects.all()

    if form.is_valid():
        search = form.cleaned_data.get('search', None)
        location = form.cleaned_data.get('location', None)
        #time = form.cleaned_data.get('time', None)
        if search:
            events = events.filter(
                Q(title__icontains=search) | Q(contentq__icontains=search)).distinct()
        if location:
            events = events.filter(location=location)
        #if time:
         #   events = events.filter(starter_date=time)

    context = {'events': events, 'form': form}
    return render(request, 'event/event_list.html', context)


@login_required(login_url='/user/login/')
def profile(request):
    user = Event.objects.filter(author=request.user)
    context = {
        "user": user
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/user/login/')
def event_create(request):
    form = EventForm()
    if request.method == 'POST':
        # print(request.POST)
        form = EventForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            msg = 'Tebrikler <strong> %s </strong> isimli gönderiniz başarı ile oluşturuldu.' % (event.title)
            messages.success(request, msg, extra_tags='success')

            return render(request, 'event/event-create.html', context={'form': form})
    return render(request, 'event/event-create.html', context={'form': form})


def event_detail(request, slug):
    form = CommentForm()
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'event/event-detail.html', context={'event': event, 'form': form})


@login_required(login_url='/user/login/')
def event_update(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.user != event.user:
        return HttpResponseForbidden
    form = EventForm(instance=event, data=request.POST or None,
                     files=request.FILES or None)  # bloğun içerisindeki değerleri çeker
    if form.is_valid():
        form.save()
        msg = 'Tebrikler %s isimli gönderiniz başarı ile güncellendi.' % (event.title)
        messages.success(request, msg, extra_tags='info')
        return HttpResponseRedirect(event.get_absolute_url())
    context = {'form': form, 'event': event}

    return render(request, 'event/event-update.html', context)


@login_required(login_url='/user/login/')
def event_delete(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.user != event.user:
        return HttpResponseForbidden
    event.delete()
    return redirect('profile')


@login_required(login_url='/user/login/')
def registerEvent(request, slug):
    event = get_object_or_404(Event, slug=slug)
    event_member = EventMember.objects.filter(event=event, user=request.user)
    if not event_member.exists():
        EventMember.objects.create(event=event, user=request.user)
    return redirect('index')


def get_child_comment_form(request):
    data = {'form_html': ''}
    pk = request.GET.get('comment_pk')
    comment = get_object_or_404(NewComment, pk=pk)
    form = CommentForm()
    form_html = render_to_string('event/include/comment/comment-child-comment-form.html', context={
        'form': form,
        'comment': comment,
    }, request=request)

    data.update({
        'form_html': form_html
    })

    return JsonResponse(data=data)


def new_add_comment(request, pk, model_type):
    data = {'is_valid': True, 'event_comment_html': '', 'model_type': model_type}

    nesne = None
    all_comment = None
    form = CommentForm(data=request.POST)

    if model_type == 'event':
        nesne = get_object_or_404(Event, pk=pk)
    elif model_type == 'comment':
        nesne = get_object_or_404(NewComment, pk=pk)
    else:
        raise Http404

    if form.is_valid():
        icerik = form.cleaned_data.get('icerik')
        NewComment.add_comment(nesne, model_type, request.user, icerik)

    if model_type == "comment":
        nesne = nesne.content_object

    comment_html = render_to_string('event/include/comment/comment-list-partial.html', context={'event': nesne})

    data.update({
        'event_comment_html': comment_html
    })

    return JsonResponse(data=data)
