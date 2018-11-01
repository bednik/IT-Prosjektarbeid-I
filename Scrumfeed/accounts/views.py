from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from accounts.forms import EditProfileForm, EditUserProfile
from django.contrib.auth import update_session_auth_hash
from .models import UserProfile
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from ScrummerTimes.models import Style


def signup_view(request):
    styles = Style.objects.filter()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            #log the user in
            return redirect('/ScrummerTimes')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html',{'form': form, 'styles':styles})

def login_view(request):
    styles = Style.objects.filter()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #log in the user
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/ScrummerTimes')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form, 'styles':styles})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/ScrummerTimes')

def profile(request):
    styles = Style.objects.filter()
    args = {'user': request.user, 'styles':styles}
    return render(request, 'accounts/profile.html', args)


def edit_userprofile(request, id=None):
    styles = Style.objects.filter()
    Up = get_object_or_404(UserProfile, pk=id)
    form = EditUserProfile()
    if request.method == "POST":
        form = EditUserProfile(request.POST, request.FILES)

        if form.is_valid():
            Up.description = form.cleaned_data["description"]
            Up.phone = form.cleaned_data["phone"]
            Up.image = form.cleaned_data["image"]

            Up.save()

            return redirect('/accounts/profile')

    context = {
        'form': form,
        'id': id,
        'styles': styles
    }

    return render(request, 'accounts/edit_profile_2.html', context)


def edit_profile(request):
    styles = Style.objects.filter()
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:edit_userprofile',kwargs={"id":request.user.userprofile.id}))

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form, 'styles':styles}
        return render(request, 'accounts/edit_profile.html', args)



def change_password(request):
    styles = Style.objects.filter()
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            return redirect('/accounts/change-password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form, 'styles':styles}
        return render(request, 'accounts/change_password.html', args)


