from django.urls import path
from . import views as SlapifyViews

urlpatterns = [
    path('', SlapifyViews.index, name='index'),
]