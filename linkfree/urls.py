from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from users.views import (
    HomeView,
    DashboardView,
    SignUpView,
    PublicProfileView,
    DeleteLinkView,
    StatsView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Pagine principali
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("stats/", StatsView.as_view(), name="stats"),

    # Auth (login/logout + signup)
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),

    # Password reset flow
    path(
        "accounts/password-reset/",
        auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
        name="password_reset",
    ),
    path(
        "accounts/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name="password_reset_complete",
    ),

    # Azioni link
    path("links/<int:pk>/delete/", DeleteLinkView.as_view(), name="link_delete"),

    # Profilo pubblico (/@username)
    path("@<str:username>/", PublicProfileView.as_view(), name="public_profile"),
]

# Static e Media (dev) | Media (prod)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # In produzione su Render per servire i media dall'app (finché usi disco effimero)
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", 
                view=auth_views.redirect_to_login.__wrapped__.__globals__['serve'],  # usa la stessa serve di django.views.static
                kwargs={"document_root": settings.MEDIA_ROOT}),
    ]
