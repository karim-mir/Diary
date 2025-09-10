from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from django.views import View

from users.forms import CustomUserRegistrationForm
from users.models import EmailConfirmation


class ConfirmEmailView(TemplateView):
    """
    Представление для подтверждения email по токену.

    Обрабатывает ссылку подтверждения и активирует учетную запись пользователя.
    """
    template_name = "users/confirmation_success.html"

    def get(self, request, token):
        """
        Обрабатывает GET-запрос для подтверждения email.

        Аргументы:
            token (str): Уникальный токен подтверждения из ссылки.

        Возвращает:
            HttpResponse: Страница успешного подтверждения или ошибки.
        """
        try:
            confirmation = EmailConfirmation.objects.get(token=token)
            user = confirmation.user
            user.is_active = True
            user.save()
            confirmation.delete()  # удаляем запись с токеном после подтверждения
            return render(request, "users/confirmation_success.html")
        except EmailConfirmation.DoesNotExist:
            return render(request, "users/confirmation_invalid.html")


class RegisterView(FormView):
    """
    Представление для регистрации пользователя с отправкой письма подтверждения.

    Создает неактивную учетную запись и отправляет письмо с ссылкой подтверждения.
    """
    template_name = "users/register.html"
    form_class = CustomUserRegistrationForm
    success_url = "/registration-pending/"

    def form_valid(self, form):
        """
        Обрабатывает валидную форму регистрации.

        Создает неактивного пользователя, генерирует токен подтверждения
        и отправляет письмо с ссылкой активации.

        Аргументы:
            form (CustomUserRegistrationForm): Валидная форма регистрации.

        Возвращает:
            HttpResponse: Перенаправление на страницу ожидания подтверждения.
        """
        user = form.save(commit=False)
        user.is_active = False  # неактивный до подтверждения email
        user.save()

        confirmation = EmailConfirmation.objects.create(user=user)

        confirm_url = self.request.build_absolute_uri(
            reverse("users:confirm_email", args=[str(confirmation.token)])
        )
        send_mail(
            "Подтверждение регистрации",
            f"Для активации учетной записи перейдите по ссылке:\n{confirm_url}",
            "your_email@example.com",
            [user.email],
        )

        return render(self.request, "users/registration_pending.html")


class LoginView(FormView):
    """
    Представление для аутентификации пользователя.

    Обрабатывает форму входа и выполняет аутентификацию.
    """
    template_name = "users/login.html"
    form_class = AuthenticationForm

    def form_valid(self, form):
        """
        Обрабатывает валидную форму аутентификации.

        Выполняет вход пользователя и перенаправляет на главную страницу.

        Аргументы:
            form (AuthenticationForm): Валидная форма аутентификации.

        Возвращает:
            HttpResponseRedirect: Перенаправление на главную страницу.
        """
        user = form.get_user()
        login(self.request, user)
        return redirect("diary:entry_list")

    def form_invalid(self, form):
        """
        Обрабатывает невалидную форму аутентификации.

        Возвращает форму с ошибками для исправления.

        Аргументы:
            form (AuthenticationForm): Невалидная форма аутентификации.

        Возвращает:
            HttpResponse: Форма с ошибками валидации.
        """
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(View):
    """
    Представление для выхода пользователя из системы.

    Выполняет logout и перенаправляет на страницу входа.
    """

    def get(self, request):
        """
        Обрабатывает GET-запрос для выхода из системы.

        Возвращает:
            HttpResponseRedirect: Перенаправление на страницу входа.
        """
        logout(request)
        return redirect("users:login")


class HomeView(TemplateView):
    """
    Представление для домашней страницы пользователя.

    Отображает главную страницу после успешного входа.
    """
    template_name = "users/home.html"
