from django.shortcuts import redirect, render
from .forms import UserAccountForm

def register(request):

    form = UserAccountForm()

    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        
    context = {'form': form}
        
    return render(request, 'useraccount/registration/register.html', context=context)
