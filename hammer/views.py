from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import View


class IndexView(View):
    def get(self, request):
        return render(request, 'hammer/index.html')


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'hammer/register.html'
    success_url = reverse_lazy('index')
