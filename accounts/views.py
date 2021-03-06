from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from .forms import UserLoginForm, UserRegistrationForm, EditProfileForm, PasswordChangingForm


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('company:home')
            else:
                messages.error(request, 'username or password is wrong !', 'danger')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            check = User.objects.filter(email__iexact=cd['email']).exists()
            if check:
                messages.error(request, 'please take another email !', 'danger')
            else:
                user = User.objects.create_user(full_name=cd['full_name'], email=cd['email'], password=cd['password1'])
                user.save()
                login(request, user)
                messages.success(request, 'you registered and login successfully', 'success')
                return redirect('company:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('company:home')


@login_required
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            user.email = form.cleaned_data['email']
            user.full_name = form.cleaned_data['full_name']
            user.save()
            messages.success(request, 'your profile edited successfully', 'success')
            return redirect('accounts:profile', user_id)
    else:
        form = EditProfileForm(instance=user.profile,
                               initial={'email': request.user.email,
                                        'full_name': request.user.full_name,
                                        'bio': request.user.profile.bio,
                                        'age': request.user.profile.age,
                                        'phone': request.user.profile.phone,
                                        'street': request.user.profile.street,
                                        'city': request.user.profile.city,
                                        'country': request.user.profile.country,
                                        'state': request.user.profile.state,
                                        'zip_code': request.user.profile.zip_code,
                                        'image': request.user.profile.image,
                                        })
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.user.password  # user's current password
        form = PasswordChangingForm(request.POST)
        if form.is_valid():
            current_password_entered = form.cleaned_data.get("old_password")
            password1 = form.cleaned_data.get("new_password1")
            match_check = check_password(current_password_entered, current_password)
            if match_check:
                request.user.set_password(password1)
                request.user.save()
                messages.success(request, 'password changed successfully!', 'success')
            else:
                messages.error(request, 'your current password entered is wrong !', 'danger')
        else:
            messages.error(request, 'please fill the form correctly !!', 'danger')
    else:
        form = PasswordChangingForm()
    return render(request, 'accounts/change-password.html', {'form': form})


@login_required
def delete_user(request):
    return render(request, 'accounts/delete-account.html')


@login_required
def delete_user_confirm(request, user_id):
    if request.user.id == user_id:
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, "Your accounts Deleted successfully ! ", 'success')
    else:
        messages.error(request, "User does not exist")
    return redirect('company:home')
