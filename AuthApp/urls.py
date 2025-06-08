# created manually!
from django.urls import path
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path('login', views.loginUser, name='login_page'),
    path('logout', views.logoutUser, name='auth-logout'),
    path('register', views.registerUser, name='auth-register'),
    path('edit-user', views.editUser, name='auth-edit-user'),
    path('delete-user', views.deleteUser, name='auth-delete-user'),
    path('edit-password', views.editPassword, name='auth-edit-password'),
    path('create-profile', views.createProfile, name='auth-create-profile'),
    path('edit-profile', views.editProfile, name='auth-edit-profile'),
    path('dashboard', views.dashboard, name='auth-dashboard'),
    path('reset-password', views.CustomPasswordResetView.as_view(), name="reset_password"), # requires email form only, PasswordResetForm
    path('reset-password-sent', authViews.PasswordResetDoneView.as_view(template_name="blogAuthApp/password-reset-done.html"), name="password_reset_done"), # just shows that password change link has been sent to your email
    path('reset/<uidb64>/<token>', views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"), # shows another form to enter a new password, SetPasswordForm
    path('reset-password-complete', authViews.PasswordResetCompleteView.as_view(template_name="blogAuthApp/password-reset-complete.html"), name="password_reset_complete"), # just shows another page where you can see a login link
]