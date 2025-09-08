from django.urls import path

from .views import confirm_email, home, register, user_login, user_logout

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("confirm_email/<uuid:token>/", confirm_email, name="confirm_email"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("home/", home, name="home"),
]
