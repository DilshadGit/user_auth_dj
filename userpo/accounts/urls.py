from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # ── Branch 1: Registration ──
    path("signup/", views.SignUpView.as_view(), name="signup"),

    # ── Branch 2: Authentication & Sessions ──
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("user/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/block/", views.block_user, name="block_user"),

    # ── Branch 3: Profile Lifecycle ──
    path("profile/", views.user_profile, name="profile"),
    path("profile/edit/", views.profile_update, name="profile_update"),
    path("profile/delete/", views.profile_delete, name="profile_delete"),

    # ── Branch 4: Password Management ──
    path(
        "password-change/",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),

    # ── Branch 5: Password Reset Lifecycle ──
    path(
        "password-reset/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]