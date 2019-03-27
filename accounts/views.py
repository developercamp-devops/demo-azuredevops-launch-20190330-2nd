from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, resolve_url
from django.views.generic import CreateView, TemplateView
from .forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup_form.html'

    def get_success_url(self):
        next_url_or_name = self.request.GET.get('next', 'profile')
        return resolve_url(next_url_or_name)

signup = SignupView.as_view()


login = LoginView.as_view(template_name='accounts/login_form.html')


profile = login_required(TemplateView.as_view(template_name='accounts/profile.html'))


logout = LogoutView.as_view()

