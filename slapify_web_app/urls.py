from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('playlist/<int:pk>', views.PlaylistDetailView.as_view(), name='playlist_details')
]