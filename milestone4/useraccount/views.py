from django.shortcuts import redirect, render
from .forms import UserAccountForm
from django.contrib.sites.shortcuts import get_current_site
from . token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def register(request):

    form = UserAccountForm()

    if request.method == 'POST':

        form = UserAccountForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            #email template set up
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


def email_verification(request):
    pass

def email_verification_sent(request):
    pass

def email_verification_success(request):
    pass

def email_verification_failed(request):
    pass