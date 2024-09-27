from django.shortcuts import redirect, render
from .forms import UserAccountForm, LoginForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

def register(request):
    form = UserAccountForm()

    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            # Email template setup
            current_site = get_current_site(request)
            email_subject = 'Activate your account'
            email_message = render_to_string('useraccount/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user)
            })

            user.email_user(email_subject, email_message)
            return redirect('email-verification-sent')

    context = {'form': form}
    return render(request, 'useraccount/registration/register.html', context=context)

def email_verification(request, uidb64, token):
    # Unique identifier
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    # Successful verification
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')

    # Failed verification
    else:
        return redirect('email-verification-failed')

def email_verification_sent(request):
    return render(request, 'useraccount/registration/email-verification-sent.html')

def email_verification_success(request):
    return render(request, 'useraccount/registration/email-verification-success.html')

def email_verification_failed(request):
    return render(request, 'useraccount/registration/email-verification-failed.html')


def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            keep_me_logged_in = form.cleaned_data.get('keep_me_logged_in')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if keep_me_logged_in:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser close
                auth.login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
            
    context = {'form': form}
    return render(request, 'useraccount/my-login.html', context=context)

def user_logout(request):
    logout(request)
    return redirect('shop')

@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'useraccount/dashboard.html')

@login_required(login_url='my-login')
def profile_management(request):

    form = UserUpdateForm(instance=request.user)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        
 

    context = {'form': form}


    return render(request, 'useraccount/profile-management.html', context=context)


@login_required(login_url='my-login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()
        return redirect('shop')

    return render(request, 'useraccount/delete-account.html')
