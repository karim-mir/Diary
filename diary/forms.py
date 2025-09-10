from django import forms
from .models import Entry, Tag


class EntryForm(forms.ModelForm):
    """
    Форма для создания и редактирования записей дневника.

    Наследует от ModelForm и использует модель Entry.
    Включает поле выбора тегов с виджетом CheckboxSelectMultiple.

    Мета:
        model (Entry): Модель, связанная с формой.
        fields (list): Поля, включаемые в форму.
        widgets (dict): Виджеты для полей формы.
    """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Entry
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
