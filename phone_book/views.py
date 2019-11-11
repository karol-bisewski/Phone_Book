from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from phone_book.forms import PhoneForm, EmailForm
from phone_book.models import Person


class PersonListView(ListView):
    model = Person
    paginate_by = 10


class PersonCreateView(CreateView):
    model = Person
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('phone_book:contacts')


class PersonUpdateView(UpdateView):
    model = Person
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('phone_book:contacts')


def delete_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if person.can_delete():
        success_url = reverse_lazy('phone_book:contacts')
        delete_view = DeleteView.as_view(model=Person, success_url=success_url)
        return delete_view(request, pk=pk)
    else:
        context = {'request': request, 'person': person}
        return render(request, 'phone_book/person_cannot_delete.html', context)


def create_phone(request, pk):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('phone_book:contacts'))
        else:
            person = get_object_or_404(Person, pk=pk)
            context = {'form': PhoneForm(initial={'person': pk}),
                       'person': person}
            return render(request, 'phone_book/phone_form.html', context)
    else:
        person = get_object_or_404(Person, pk=pk)
        context = {'form': PhoneForm(initial={'person': pk}),
                   'person': person}
        return render(request, 'phone_book/phone_form.html', context)


def create_email(request, pk):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('phone_book:contacts'))
        else:
            person = get_object_or_404(Person, pk=pk)
            context = {'form': EmailForm(initial={'person': person}),
                       'person': person}
            return render(request, 'phone_book/email_form.html', context)
    else:
        person = get_object_or_404(Person, pk=pk)
        context = {'form': EmailForm(initial={'person': person}),
                   'person': person}
        return render(request, 'phone_book/email_form.html', context)


class PersonSearch(PersonListView):
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.GET['q']:
            q = self.request.GET['q']
        return self.model.objects\
                   .annotate(full_name=Concat('first_name', Value(' '), 'last_name'))\
                   .filter(Q(full_name__icontains=q)
                           | Q(email__email__icontains=q)
                           | Q(phone__phone__icontains=q)).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET['q']
        return context
