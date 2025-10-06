from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from vagas.forms import VagaModelForm
from vagas.models import Vaga


class VagasView(ListView):
    model = Vaga
    template_name = 'vagas.html'
    context_object_name = 'vagas'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(codigo__icontains=buscar)
        return queryset


class VagaAddView(SuccessMessageMixin, CreateView):
    model = Vaga
    form_class = VagaModelForm
    template_name = 'vaga_form.html'
    success_url = reverse_lazy('vagas')
    success_message = 'Vaga cadastrada com sucesso!'


class VagaUpdateView(SuccessMessageMixin, UpdateView):
    model = Vaga
    form_class = VagaModelForm
    template_name = 'vaga_form.html'
    success_url = reverse_lazy('vagas')
    success_message = 'Vaga alterada com sucesso!'


class VagaDeleteView(SuccessMessageMixin, DeleteView):
    model = Vaga
    template_name = 'vaga_apagar.html'
    success_url = reverse_lazy('vagas')
    success_message = 'Vaga excluída com sucesso!'

    def post(self, request, *args, **kwargs):
        vaga = self.get_object()
        if vaga.status == 'ocupada':
            messages.error(request, f'A vaga "{vaga.codigo}" está em uso e não pode ser apagada.')
            return redirect('vagas')
        return super().post(request, *args, **kwargs)
