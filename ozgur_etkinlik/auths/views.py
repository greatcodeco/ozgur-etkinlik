from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, reverse
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm, UserProfileUpdateForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from events.models import Event, FavoriteEvent
from django.template.loader import render_to_string


# Create your views here.

def register(request):
    form = RegisterForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

    return render(request, 'auths/register.html', context={'form': form})


def user_login(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

    return render(request, 'auths/login.html', context={'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    data = {'html': ''}

    page = request.GET.get('page1', 1)
    event_list = Event.objects.filter(user=user)
    event_list_count = event_list.count()
    favorite_events = FavoriteEvent.objects.filter(user=user)

    event_list = events_and_favorite_events_paginate(event_list, page)
    page2 = request.GET.get('page2', 1)
    favorite_events = events_and_favorite_events_paginate(favorite_events, page2)
    context = {'user': user, 'event_list': event_list, 'event_list_count': event_list_count,
               'favorite_events': favorite_events,
               'page': 'user-profile'}

    if request.is_ajax():

        html_events = render_to_string('auths/profile/include/profile_events_list.html', context=context)
        html_favorite = render_to_string('auths/profile/include/profile_favorite_events_list.html', context=context)
        data.update({'html': html_events, 'html_favorite': html_favorite})
        return JsonResponse(data=data)

    return render(request, 'auths/profile/userprofile.html', context=context)


def user_profile_update(request):
    sex = request.user.userprofile.sex
    bio = request.user.userprofile.bio
    profile_photo = request.user.userprofile.profile_photo
    birth_day = request.user.userprofile.birth_day

    initial = {'sex': sex, 'bio': bio, 'profile_photo': profile_photo, 'birth_day': birth_day}
    form = UserProfileUpdateForm(initial=initial, instance=request.user, data=request.POST or None,
                                 files=request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=True)
            bio = form.cleaned_data.get('bio', None)
            sex = form.cleaned_data.get('sex', None)
            profile_photo = form.cleaned_data.get('profile_photo', None)
            birth_day = form.cleaned_data.get('birth_day', None)

            user.userprofile.sex = sex
            user.userprofile.profile_photo = profile_photo
            user.userprofile.bio = bio
            user.userprofile.birth_day = birth_day
            user.userprofile.save()
            messages.success(request, 'Tebrikler Kullanıcı Bilgileriniz Başarıyla Güncellendi', extra_tags='success')
            return HttpResponseRedirect(reverse('user-profile', kwargs={'username': user.username}))
        else:
            messages.warning(request, 'Lütfen form alanlarını doğru giriniz.', extra_tags='danger')

    return render(request, 'auths/profile/settings.html', context={'form': form})


def profile_list_events(request):
    data = {'sa': 'sa'}
    selam = "selamet"
    context = {'selam': selam}

    return render(request, 'auths/profile/include/sa.html', context=context)


def events_and_favorite_events_paginate(queryset, page):
    paginator = Paginator(queryset, 1)
    try:
        queryset = paginator.page(page)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        queryset = paginator.page(1)

    return queryset
