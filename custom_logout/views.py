from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)
    messages.add_message(
        request,
        messages.INFO,
        'Logged out'
    )
    return redirect('home')
