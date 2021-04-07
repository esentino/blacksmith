from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views.generic.base import View

from hammer.models import Blacksmith, Task

MAX_TASKS_COUNT = 4


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "hammer/index.html")


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "hammer/register.html"
    success_url = reverse_lazy("index")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "hammer/profile.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs = super().get_context_data(**kwargs)
        try:
            if isinstance(self.request.user, User):
                blacksmith = self.request.user.blacksmith
                for task in blacksmith.tasks.all():
                    task.process()
                blacksmith.refresh_from_db()
                kwargs["blacksmith"] = blacksmith
                self.prepare_tasks_for_blacksmith(blacksmith)
        except Blacksmith.DoesNotExist:
            pass
        return kwargs

    @staticmethod
    def prepare_tasks_for_blacksmith(blacksmith: Blacksmith) -> None:
        count = Task.objects.filter(blacksmith=blacksmith).count()
        if count >= MAX_TASKS_COUNT:
            return
        for i in range(MAX_TASKS_COUNT - count):
            Task.generate_task(blacksmith)


class CreateBlacksmith(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if isinstance(request.user, User) and not Blacksmith.objects.filter(owner=request.user).exists():
            Blacksmith.objects.create(owner=request.user)
        return redirect("profile")


class StartTask(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, task_id: int) -> HttpResponse:
        task = get_object_or_404(Task, pk=task_id)
        if task.can_start:
            task.start()
            messages.success(request, "Task started")
        else:
            messages.error(request, "Can't start task other task in progress")
        return redirect("profile")


class AddHeatingAttributeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if isinstance(request.user, User):
            added = request.user.blacksmith.add_heating_attribute()
            if added:
                messages.success(request, "Attribute added")
        return redirect("profile")


class AddHoldingAttributeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if isinstance(request.user, User):
            added = request.user.blacksmith.add_holding_attribute()
            if added:
                messages.success(request, "Attribute added")
        return redirect("profile")


class AddHittingAttributeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if isinstance(request.user, User):
            added = request.user.blacksmith.add_hitting_attribute()
            if added:
                messages.success(request, "Attribute added")
        return redirect("profile")


class AddShapingAttributeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if isinstance(request.user, User):
            added = request.user.blacksmith.add_shaping_attribute()
            if added:
                messages.success(request, "Attribute added")
        return redirect("profile")
