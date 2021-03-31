from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views.generic.base import View

from hammer.models import Blacksmith


class IndexView(View):
    def get(self, request):
        return render(request, 'hammer/index.html')


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'hammer/register.html'
    success_url = reverse_lazy('index')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'hammer/profile.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        blacksmith = self.request.user.blacksmith
        if blacksmith:
            kwargs['blacksmith'] = blacksmith
        return kwargs


class CreateBlacksmith(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.blacksmith is None:
            Blacksmith.objects.create(owner=request.user)
        return redirect('profile')
