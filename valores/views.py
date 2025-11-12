from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from valores.forms import PlanoForm, DescontoForm, ExtraForm, CategoriaForm
from valores.models import Plano, Desconto, Extra, Categoria
from veiculos.models import Veiculo

    # ------ CRUD  Planos
class PlanosView(PermissionRequiredMixin, ListView):
    permission_required = "valores.view_planos"
    permission_denied_required = "Visualizar planos"
    model = Plano
    template_name = "planos/planos.html"
    context_object_name = "planos"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            qs = qs.filter(
                Q(plano__icontains=buscar) |
                Q(status__icontains=buscar)
            )
        return qs

class PlanoCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "valores.add_plano"
    permission_denied_required = "Cadastrar plano"
    model = Plano
    form_class = PlanoForm
    template_name = "planos/planos_form.html"
    success_url = reverse_lazy('planos')
    success_message = "Plano cadastrado com sucesso."

class PlanoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "valores.update_plano"
    permission_denied_required = "Atualizar plano."
    model = Plano
    form_class = PlanoForm
    template_name = "planos/planos_form.html"
    success_url = reverse_lazy('planos')
    success_message = "Plano atualizado com sucesso."

class PlanoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "valores.delete_plano"
    permission_denied_message = "Apagar plano"
    model = Plano
    template_name = "planos/plano_apagar.html"
    success_url = reverse_lazy('planos')
    success_message = "Plano apagado com sucesso"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plano_obj = self.get_object()
        contagem = Veiculo.objects.filter(plano=plano_obj).count()
        context['veiculos_count'] = contagem
        return context


    # ----- CRUD Descontos


class DescontosView(PermissionRequiredMixin, ListView):
    permission_required = "valores.view_descontos"
    permission_denied_required = "Visualizar descontos"
    model = Desconto
    template_name = "descontos/descontos.html"
    context_object_name = "descontos"
    paginate_by = 5

    def get_queryset(self):
        self.regras_negocio_descontos()

        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            qs = qs.filter(
                Q(nome__icontains=buscar) |
                Q(descricao__icontains=buscar) |
                Q(status__icontains=buscar)
            )
        return qs

    def regras_negocio_descontos(self):
        if Desconto.objects.exists():
            return

        descontos_padrao = [
            {
                 'codigo_interno': 'DESCONTO_FUNCIONARIO',
            'nome': 'Desconto Funcionário',
            'tipo': 'PERCENTUAL',
            'valor': 20.00,
            'descricao': 'Desconto de 20% para funcionários',
            'status': True
        },
        {
            'codigo_interno': 'DESCONTO_PIX_DINHEIRO',
            'nome': 'Desconto PIX/Dinheiro',
            'tipo': 'PERCENTUAL',
            'valor': 15.00,
            'descricao': 'Desconto de 15% para pagamentos em PIX ou Dinheiro',
            'status': True
            },
        ]

        for dados in descontos_padrao:
            Desconto.objects.get_or_create(
                codigo_interno=dados['codigo_interno'],
                defaults=dados
            )

class DescontoCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "valores.add_desconto"
    permission_denied_required = "Cadastrar desconto"
    model = Desconto
    form_class = DescontoForm
    template_name = "descontos/desconto_form.html"
    success_url = reverse_lazy('descontos')
    success_message = "Desconto cadastrado com sucesso."

class DescontoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "valores.update_desconto"
    permission_denied_required = "Atualizar desconto"
    model = Desconto
    form_class = DescontoForm
    template_name = "descontos/desconto_form.html"
    success_url = reverse_lazy('descontos')
    success_message = "Desconto atualizado com sucesso."

class DescontoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "valores.delete_desconto"
    permission_denied_required = "Apagar desconto"
    model = Desconto
    form_class = DescontoForm
    template_name = "descontos/desconto_apagar.html"
    success_url = reverse_lazy('descontos')
    success_message = "Desconto apagado com sucesso."


    # ----- CRUD Extras

class ExtraView(PermissionRequiredMixin, ListView):
    permission_required = "valores.view_extra"
    permission_denied_message = "Listar valores extras"
    model = Extra
    template_name = "extras/extras.html"
    context_object_name = "extras"
    paginate_by = 5

    def get_queryset(self):
        self.regras_negocio_extra()

        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            qs = qs.filter(
                Q(nome__icontains=buscar) |
                Q(status__icontains=buscar)
            )
        return qs

    def regras_negocio_extra(self):
        if Extra.objects.exists():
            return

        extras_padrao = [
            {
                'nome': 'Multa Tempo Excedido',
                'tipo': 'PERCENTUAL',
                'valor': 50.00,
                'descricao': 'Multa de 50% para estadias acima de 12 horas',
                'status': True
            },
        ]

        for dados in extras_padrao:
            Extra.objects.get_or_create(
                nome=dados['nome'],
                defaults=dados
            )

class ExtraCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "valores.add_extra"
    permission_denied_message = "Cadastrar valor extra"
    model = Extra
    form_class = ExtraForm
    template_name = "extras/extra_form.html"
    success_url = reverse_lazy('extras')
    success_message = "Valor extra cadastrado com sucesso."

class ExtraUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "valores.update_extra"
    permission_denied_message = "Atualizar valor extra"
    model = Extra
    form_class = ExtraForm
    template_name = "extras/extra_form.html"
    success_url = reverse_lazy('extras')
    success_message = "Valor extra atualizado com sucesso."

class ExtraDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "valores.delete_extra"
    permission_denied_message = "Apagar valor extra"
    model = Extra
    template_name = "extras/extra_apagar.html"
    success_url = reverse_lazy('extras')
    success_message = "Valor extra apagado com sucesso."


    # ----- CRUD Categoria


class CategoriaView(PermissionRequiredMixin, ListView):
    permission_required = "valores.view_categoria"
    permission_denied_message = "Listar categorias"
    model = Categoria
    template_name = "categorias/categorias.html"
    context_object_name = "categorias"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            qs = qs.filter(
                Q(nome__icontains=buscar) |
                Q(status__icontains=buscar)
            )
        return qs

class CategoriaCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "valores.add_categoria"
    permission_denied_message = "Cadastrar categorias"
    model = Categoria
    form_class = CategoriaForm
    template_name = "categorias/categoria_form.html"
    success_url = reverse_lazy('categorias')
    success_message = "Categoria cadastrada com sucesso."

class CategoriaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "valores.update_categoria"
    permission_denied_message = "Atualizar categorias"
    model = Categoria
    form_class = CategoriaForm
    template_name = "categorias/categoria_form.html"
    success_url = reverse_lazy('categorias')
    success_message = "Categoria atualizada com sucesso."

class CategoriaDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "valores.delete_categoria"
    permission_denied_message = "Apagar categorias"
    model = Categoria
    template_name = "categorias/categoria_apagar.html"
    success_url = reverse_lazy('categorias')
    success_message = "Categoria apagada com sucesso."