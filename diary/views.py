from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Entry

class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    context_object_name = 'entries'
    template_name = 'diary/entry_list.html'

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user).order_by('-created_at')


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    context_object_name = 'entry'
    template_name = 'diary/entry_detail.html'

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    fields = ['title', 'content']
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('diary:entry_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    fields = ['title', 'content']
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('diary:entry_list')

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit'
        return context


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'diary/entry_confirm_delete.html'
    success_url = reverse_lazy('diary:entry_list')

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)
