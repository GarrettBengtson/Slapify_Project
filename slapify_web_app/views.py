from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Playlist, Song
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    user_playlists = Playlist.objects.filter(user=request.user)

    context = {
        'user_playlists': user_playlists,
    }
    return render(request, 'index.html', context)

class PlaylistDetailView(generic.DetailView):
    """Lists songs in the playlist"""
    model = Playlist
    template_name = 'playlist_view.html'

    def get_queryset(self):
        return(
            Playlist.objects.filter(user=self.request.user)
        )

class CreatePlaylistView(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ['name']

    # redirect the user
    success_url = reverse_lazy('index')

    # set the 'user' attriubute of Playlist to the logged in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    