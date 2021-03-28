from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render('hammer/index.html')
