from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import CustomUserRegistrationForm
from users.models import EmailConfirmation


def confirm_email(request, token):
    """Обработка ссылки подтверждения email"""
    try:
        confirmation = EmailConfirmation.objects.get(token=token)
        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()  # удаляем запись с токеном после подтверждения
        return render(request, "users/confirmation_success.html")
    except EmailConfirmation.DoesNotExist:
        return render(request, "users/confirmation_invalid.html")


def register(request):
    """Регистрация пользователя с отправкой письма подтверждения"""
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # неактивный до подтверждения email
            user.save()

            confirmation = EmailConfirmation.objects.create(user=user)

            confirm_url = request.build_absolute_uri(
                reverse("users:confirm_email", args=[str(confirmation.token)])
            )
            send_mail(
                "Подтверждение регистрации",
                f"Для активации учетной записи перейдите по ссылке:\n{confirm_url}",
                "your_email@example.com",
                [user.email],
            )

            return render(request, "users/registration_pending.html")
    else:
        form = CustomUserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("diary:base")  # или нужная вам страница
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("users:login")


def home(request):
    return render(request, "users/home.html")
