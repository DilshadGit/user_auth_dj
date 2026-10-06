from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.utils import timezone
from django.utils.html import escape

from .forms import EmailLoginForm, ProfileUpdateForm, SignUpForm
from .models import ProfileUpdateLog

User = get_user_model()


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject='Welcome to AccountCMS',
            message=(
                f'Hello {user.first_name or user.email},\n\n'
                'Your account has been created successfully.\n'
                'You can now sign in to your profile and manage your account securely.\n\n'
                f'Email: {user.email}\n'
                'If you ever need to reset your password, use the forgot password link on the login page.\n'
            ),
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )
        login(self.request, user, backend='accounts.backends.EmailBackend')
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    authentication_form = EmailLoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return reverse_lazy('accounts:dashboard')
        return reverse_lazy('accounts:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        ip = self.request.META.get('HTTP_X_FORWARDED_FOR') or self.request.META.get('REMOTE_ADDR')
        if ip:
            user.last_login_ip = ip.split(',')[0].strip()
            user.save(update_fields=['last_login_ip'])
        return response


class CustomLogoutView(LogoutView):
    template_name = "accounts/logout.html"
    http_method_names = ["get", "post", "options"]
    next_page: str | None = "accounts:login"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_logout_at = timezone.now()
            request.user.save(update_fields=['last_logout_at'])
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change_form.html"
    success_url = reverse_lazy("accounts:password_change_done")


class CustomPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset_form.html"
    email_template_name = "accounts/emails/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_active or request.user.is_deleted:
            messages.error(request, 'This account is inactive.')
            return redirect('accounts:login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'Only staff and admins can view the dashboard.')
            return redirect('accounts:profile')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '').strip()

        users = User.objects.order_by('-date_joined', 'email')
        if search_query:
            users = users.filter(
                Q(email__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(mobile_number__icontains=search_query)
                | Q(barcode_number__icontains=search_query)
            )

        paginator = Paginator(users, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['search_query'] = search_query
        context['page_obj'] = page_obj
        context['users_page'] = page_obj.object_list
        context['total_users'] = users.count()
        context['admin_count'] = User.objects.filter(is_superuser=True).count()
        context['staff_count'] = User.objects.filter(is_staff=True, is_superuser=False).count()
        context['member_count'] = User.objects.filter(is_staff=False, is_superuser=False).count()
        return context


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'accounts/user_detail.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = get_object_or_404(User, pk=self.kwargs['pk'])
        context['can_manage_user'] = (
            self.request.user.is_superuser or (
                self.request.user.is_staff and not context['user_detail'].is_superuser
            )
        )
        return context


@login_required
def block_user(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Only staff and admins can manage user access.')
        return redirect('accounts:profile')

    user_to_update = get_object_or_404(User, pk=pk)
    if user_to_update.is_superuser and not request.user.is_superuser:
        messages.error(request, 'Only admins can manage admin accounts.')
        return redirect('accounts:user_detail', pk=user_to_update.pk)

    user_to_update.is_active = not user_to_update.is_active
    user_to_update.save(update_fields=['is_active'])
    action = 'blocked' if not user_to_update.is_active else 'unblocked'
    messages.success(request, f'{user_to_update.email} was {action}.')
    return redirect('accounts:user_detail', pk=user_to_update.pk)


class AdminDocsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'docs/index.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        filename = kwargs.get('filename')
        if filename:
            docs_dir = Path(settings.BASE_DIR) / 'docs'
            file_path = docs_dir / filename
            if file_path.exists() and file_path.is_file() and request.user.is_superuser:
                context = self.get_context_data(**kwargs)
                context['selected_file'] = filename
                context['selected_content'] = file_path.read_text(encoding='utf-8', errors='replace')
                return render(request, self.template_name, context)
            return HttpResponseForbidden('You are not allowed to view this document.')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docs_dir = Path(settings.BASE_DIR) / 'docs'
        files = []
        if docs_dir.exists():
            for file_path in sorted(docs_dir.iterdir(), key=lambda p: p.name.lower()):
                if file_path.is_file():
                    files.append({
                        'name': file_path.name,
                        'size': file_path.stat().st_size,
                    })
        context['docs_files'] = files
        return context


@login_required
def user_profile(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user,
    })


@login_required
def profile_update(request):
    if request.method == 'POST':
        original_user = User.objects.get(pk=request.user.pk)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            old_values = {
                field: getattr(original_user, field)
                for field in ['first_name', 'last_name', 'mobile_number', 'address', 'postcode', 'date_of_birth', 'bio', 'profile_image']
            }
            user = form.save(commit=False)
            for field in old_values:
                old_value = old_values[field]
                new_value = getattr(user, field)
                if old_value != new_value:
                    ProfileUpdateLog.objects.create(
                        user=request.user,
                        field_name=field,
                        old_value=str(old_value) if old_value is not None else '',
                        new_value=str(new_value) if new_value is not None else '',
                        updated_by=request.user.email,
                    )
            user.save()
            messages.success(request, 'Your profile was updated successfully. Previous values were recorded for security history.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile_update.html', {
        'form': form,
        'user': request.user,
    })


@login_required
def profile_delete(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.is_deleted = True
        user.deleted_at = timezone.now()
        user.save(update_fields=['is_active', 'is_deleted', 'deleted_at'])
        logout(request)
        messages.success(request, 'Your account was archived and kept on record. It is no longer active.')
        return redirect('accounts:login')

    return render(request, 'accounts/profile_delete_confirm.html', {
        'user': request.user,
    })
  