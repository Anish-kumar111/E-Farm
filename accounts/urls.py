from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('', views.enquiry, name="enquiry"),
    path('profile/', views.profile, name="profile"),
    
    

        # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             
             template_name='password-reset/password_reset_form.html',
             subject_template_name='password-reset/password_reset_subject.txt',
             email_template_name='password-reset/password_reset_email.html',
             success_url='done/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password-reset/password_reset_confirm.html',
             success_url='/accounts/password-reset-complete/'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

# urlpatterns = [
#     path('login/', views.login, name='login'),
#     path('register_verify/', views.register_verify, name='register_verify'),
#     path('logout', views.logout, name='logout'),

# ]