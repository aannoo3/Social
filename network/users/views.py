from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from blog.models import Post
from django.contrib import messages
from . models import Profile, Relationship
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get('email')
            user.is_active = False  # Set inactive until email is confirmed
            user.save()

            # Send activation email
            current_site = 'localhost:8000'  # Use your domain in production
            subject = 'Activate Your Account'
            message = render_to_string('users/activation_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return redirect('email_verification')  # Redirect to a new page that tells the user to verify email
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def email_verification(request):
    return render(request, 'users/email_verification.html')




def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')  # Redirect to login page after activation
    else:
        return render(request, 'users/activation_invalid.html')  # Invalid activation link




@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user_profile)
    posts = Post.objects.filter(author=user_profile)
    is_following = Relationship.objects.filter(follower=request.user, following=user_profile).exists() if request.user.is_authenticated else False
    context = {
        'profile_user': user_profile,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'users/profile.html', context)

@login_required
def follow_unfollow(request, username):
    target_user = get_object_or_404(User, username=username)
    relationship, created = Relationship.objects.get_or_create(
        follower=request.user,
        following=target_user
    )
    if not created:
        relationship.delete()
    return HttpResponseRedirect(reverse('profile', args=[username]))

@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)  # Redirect to prevent re-submission

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile_update.html', context)