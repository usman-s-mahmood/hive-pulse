# created manually!
from . import views
from django.urls import path

urlpatterns = [
    path('login', views.login_user, name='auth-login'),
    path('logout', views.logout_user, name='auth-logout'),
    path('register', views.register_user, name='auth-register'),
    path('edit-user', views.edit_user, name='auth-edit-user'),
    path('edit-password', views.edit_password, name='auth-edit-password'),
    path('delete-user', views.delete_user, name='auth-delete-user'),
    path('create-profile', views.create_profile, name='auth-create-profile'),
    path('edit-profile', views.edit_profile, name='auth-edit-profile'),
    path('dashboard', views.user_dashboard, name='auth-dashboard'),
    # forgot password URLs
    path(
        'reset-password', 
        views.CustomPasswordResetView.as_view(), 
        name="reset_password"
    ), # requires email form only, PasswordResetForm
    path(
        'reset-password-sent', 
        views.auth_views.PasswordResetDoneView.as_view(
            template_name="AuthApp/forgot-password/password-reset-done.html"
        ), 
        name="password_reset_done"
    ), # just shows that password change link has been sent to your email
    path(
        'reset/<uidb64>/<token>', 
        views.CustomPasswordResetConfirmView.as_view(), 
        name="password_reset_confirm"
    ), # shows another form to enter a new password, SetPasswordForm
    path(
        'reset-password-complete', 
        views.auth_views.PasswordResetCompleteView.as_view(
            template_name="AuthApp/forgot-password/password-reset-complete.html"
        ), 
        name="password_reset_complete"
    ), # just shows another page where you can see a login link
    # path('email-duplication/<str:email>', views.email_duplication, name='auth-email-duplication'),
]