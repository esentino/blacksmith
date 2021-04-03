from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views.generic.base import View

from hammer.models import Blacksmith, Task


class IndexView(View):
    def get(self, request):
        return render(request, "hammer/index.html")


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "hammer/register.html"
    success_url = reverse_lazy("index")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "hammer/profile.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        try:
            blacksmith = self.request.user.blacksmith
            kwargs["blacksmith"] = blacksmith
            count = Task.objects.filter(blacksmith=blacksmith).count()
            if count < 4:
                for i in range(4 - count):
                    Task.generate_task(blacksmith)
        except Blacksmith.DoesNotExist:
            pass
        return kwargs


class CreateBlacksmith(LoginRequiredMixin, View):
    def get(self, request):
        if not Blacksmith.objects.filter(owner=request.user).exists():
            Blacksmith.objects.create(owner=request.user)
        return redirect("profile")
