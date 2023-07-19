from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import NoteForm
from .models import Note


class Home(generic.TemplateView):
    """Домашняя страница."""
    template_name = 'notes/home.html'


class NoteSuccess(LoginRequiredMixin, generic.TemplateView):
    """Страница успешного выполнения операции."""
    template_name = 'notes/success.html'


class NoteBase(LoginRequiredMixin):
    """Базовый класс для остальных CBV."""
    model = Note
    success_url = reverse_lazy('notes:success')

    def get_queryset(self):
        """Пользователь может работать только со своими заметками."""
        return self.model.objects.filter(author=self.request.user)


class NoteCreate(NoteBase, generic.CreateView):
    """Добавление заметки."""
    template_name = 'notes/form.html'
    form_class = NoteForm

    def form_valid(self, form):
        new_note = form.save(commit=False)
        new_note.author = self.request.user
        new_note.save()
        return super().form_valid(form)


class NoteUpdate(NoteBase, generic.UpdateView):
    """Редактирование заметки."""
    template_name = 'notes/form.html'
    form_class = NoteForm


class NoteDelete(NoteBase, generic.DeleteView):
    """Удаление заметки."""
    template_name = 'notes/delete.html'


class NotesList(NoteBase, generic.ListView):
    """Список всех заметок пользователя."""
    template_name = 'notes/list.html'


class NoteDetail(NoteBase, generic.DetailView):
    """Заметка подробно."""
    template_name = 'notes/detail.html'
