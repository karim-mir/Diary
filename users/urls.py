from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('confirm-email/<str:token>/', views.ConfirmEmailView.as_view(), name='confirm_email'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('registration-pending/', views.TemplateView.as_view(
        template_name='users/registration_pending.html'), name='registration_pending'),
]
