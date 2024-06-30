from django import http
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .models import UserToken


class RegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password'
    ]

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form['password'].value())
        self.object.is_active = False
        self.object.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Registration was successfull.\n'
            'Email message was sent to validate your email'
        )
        return http.HttpResponseRedirect(self.get_success_url())


def email_verification(request):
    token = request.GET.get('token')
    token = UserToken.objects.filter(token=token)
    if not token.exists():
        messages.add_message(
            request,
            messages.ERROR,
            'Token is invalid'
        )
        return redirect('home')
    token = token.first()
    user = token.user
    user.is_active = True
    user.save()
    messages.add_message(
        request,
        messages.SUCCESS,
        'Your email was confirmed. Please login'
    )
    return redirect('login')
