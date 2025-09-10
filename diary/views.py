from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from django.db.models import Q  # ← Добавьте этот импорт
from .models import Entry
from .forms import EntryForm


class EntryListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка всех записей текущего пользователя.

    Требует аутентификации. Фильтрует записи по автору и сортирует
    по дате создания (сначала новые).

    Атрибуты:
        model (Model): Модель Entry для работы с записями.
        context_object_name (str): Имя переменной контекста для шаблона.
        template_name (str): Путь к шаблону списка записей.
    """
    model = Entry
    context_object_name = "entries"
    template_name = "diary/entry_list.html"

    def get_queryset(self):
        """
        Возвращает отфильтрованный queryset записей.

        Фильтрует записи по текущему пользователю и сортирует
        по дате создания в обратном порядке. Добавлена поддержка поиска.

        Возвращает:
            QuerySet: Записи текущего пользователя, отсортированные по дате.
        """
        queryset = Entry.objects.filter(author=self.request.user).order_by("-created_at")

        # Добавлен поиск по заголовку и содержанию
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        return queryset


class EntryDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения детальной информации о записи.

    Требует аутентификации. Проверяет, что запись принадлежит
    текущему пользователю.

    Атрибуты:
        model (Model): Модель Entry для работы с записями.
        context_object_name (str): Имя переменной контекста для шаблона.
        template_name (str): Путь к шаблону детальной информации.
    """
    model = Entry
    context_object_name = "entry"
    template_name = "diary/entry_detail.html"

    def get_queryset(self):
        """
        Возвращает отфильтрованный queryset для проверки прав доступа.

        Обеспечивает, что пользователь может просматривать только свои записи.

        Возвращает:
            QuerySet: Записи текущего пользователя.
        """
        return Entry.objects.filter(author=self.request.user)


class EntryCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новой записи дневника.

    Требует аутентификации. Использует кастомную форму EntryForm
    с поддержкой тегов.

    Атрибуты:
        model (Model): Модель Entry для работы с записями.
        form_class (Form): Класс формы для создания записи.
        template_name (str): Путь к шаблону формы.
        success_url (str): URL для перенаправления после успешного создания.
    """
    model = Entry
    form_class = EntryForm
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('diary:entry_list')

    def form_valid(self, form):
        """
        Обрабатывает валидную форму создания записи.

        Устанавливает автора записи как текущего пользователя
        перед сохранением формы.

        Аргументы:
            form (EntryForm): Валидная форма записи.

        Возвращает:
            HttpResponse: Результат родительского метода form_valid.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст шаблона.

        Добавляет переменную 'action' для отображения соответствующего
        заголовка в форме.

        Возвращает:
            dict: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['action'] = 'Создать'
        return context


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования существующей записи.

    Требует аутентификации. Проверяет права доступа к записи
    и использует кастомную форму EntryForm.

    Атрибуты:
        model (Model): Модель Entry для работы с записями.
        form_class (Form): Класс формы для редактирования записи.
        template_name (str): Путь к шаблону формы.
        success_url (str): URL для перенаправления после успешного редактирования.
    """
    model = Entry
    form_class = EntryForm
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('diary:entry_list')

    def get_queryset(self):
        """
        Возвращает отфильтрованный queryset для проверки прав доступа.

        Обеспечивает, что пользователь может редактировать только свои записи.

        Возвращает:
            QuerySet: Записи текущего пользователя.
        """
        return Entry.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст шаблона.

        Добавляет переменную 'action' для отображения соответствующего
        заголовка в форме.

        Возвращает:
            dict: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['action'] = 'Редактировать'
        return context


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления записи дневника.

    Требует аутентификации. Проверяет права доступа к записи
    перед удалением.

    Атрибуты:
        model (Model): Модель Entry для работы с записями.
        template_name (str): Путь к шаблону подтверждения удаления.
        success_url (str): URL для перенаправления после успешного удаления.
    """
    model = Entry
    template_name = 'diary/entry_confirm_delete.html'
    success_url = reverse_lazy('diary:entry_list')

    def get_queryset(self):
        """
        Возвращает отфильтрованный queryset для проверки прав доступа.

        Обеспечивает, что пользователь может удалять только свои записи.

        Возвращает:
            QuerySet: Записи текущего пользователя.
        """
        return Entry.objects.filter(author=self.request.user)


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Представление для главной страницы приложения.

    Требует аутентификации. Отображает базовый шаблон или может быть
    расширено для показа последних записей и другой информации.

    Атрибуты:
        template_name (str): Путь к шаблону главной страницы.
    """
    template_name = "diary/home.html"

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст шаблона.

        Может быть расширен для добавления последних записей,
        статистики или другой информации на главную страницу.

        Возвращает:
            dict: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['recent_entries'] = Entry.objects.filter(
            author=self.request.user
        ).order_by('-created_at')[:5]
        return context
