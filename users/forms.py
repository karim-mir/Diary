from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserRegistrationForm(UserCreationForm):
    """
    Кастомная форма регистрации пользователя с аутентификацией по email.

    Наследует от UserCreationForm и добавляет обязательное поле email
    вместо стандартного username.

    Атрибуты:
        email (EmailField): Поле для ввода email адреса (обязательное)
    """

    email = forms.EmailField(label="Email", required=True)

    class Meta:
        """
        Мета-класс для настройки формы.

        Определяет:
        - model: Кастомная модель пользователя
        - fields: Поля, включаемые в форму (только email)
        """
        model = User
        fields = ("email",)

    def save(self, commit=True):
        """
        Сохраняет данные формы и создает нового пользователя.

        Переопределяет стандартный метод save для корректной работы
        с кастомной моделью пользователя и полем email.

        Аргументы:
            commit (bool): Флаг immediate сохранения в базу данных

        Возвращает:
            User: Созданный объект пользователя
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
