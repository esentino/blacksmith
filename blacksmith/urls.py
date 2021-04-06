"""blacksmith URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from hammer.views import (
    AddHeatingAttributeView,
    AddHittingAttributeView,
    AddHoldingAttributeView,
    AddShapingAttributeView,
    CreateBlacksmith,
    IndexView,
    ProfileView,
    RegisterView,
    StartTask,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/create", RegisterView.as_view(), name="register"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("accounts/create/blacksmith", CreateBlacksmith.as_view(), name="create-blacksmith"),
    path("accounts/task/start/<int:task_id>", StartTask.as_view(), name="start-task"),
    path("accounts/profile/add/heating", AddHeatingAttributeView.as_view(), name="add-heating"),
    path("accounts/profile/add/holding", AddHoldingAttributeView.as_view(), name="add-holding"),
    path("accounts/profile/add/hitting", AddHittingAttributeView.as_view(), name="add-hitting"),
    path("accounts/profile/add/shaping", AddShapingAttributeView.as_view(), name="add-shaping"),
]
