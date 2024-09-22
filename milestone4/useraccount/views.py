from django.shortcuts import render
from django.http import HttpResponse

def register(request):
    try:
        return render(request, 'useraccount/registration/register.html')
    except Exception as e:
        return HttpResponse(f"Error: {e}")
