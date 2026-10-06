from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

from .forms import EmailLoginForm, SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        user = form.save()
        # Log the user in directly after registration
        login(self.request, user)
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    authentication_form = EmailLoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard.html"

    def test_func(self):
        # Only allow verified users
        return self.request.user.is_verified
  

def user_profile(request):
    return render(request, 'accounts/profile.html')
  