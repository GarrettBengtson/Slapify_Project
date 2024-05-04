from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .models import Playlist, Song, UserRequest, AdminEdit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

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

    # allow the playlist detail page to have access to the user's playlists
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_playlists'] = Playlist.objects.filter(user=self.request.user)
        return context
    
    def get_queryset(self):
        return(
            Playlist.objects.filter(user=self.request.user)
        )

class CreatePlaylistView(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ['name']

    # redirect the user to index
    success_url = reverse_lazy('index')

    # allow the create page to have access to the user's playlists
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_playlists'] = Playlist.objects.filter(user=self.request.user)
        return context
    
    # set the 'user' attribute of Playlist to the logged in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeletePlaylistView(LoginRequiredMixin, DeleteView):
    model = Playlist

    # redirect the user to index
    success_url = reverse_lazy('index')

    # allow the delete page to have access to the user's playlists
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_playlists'] = Playlist.objects.filter(user=self.request.user)
        return context
    
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("delete_playlist", kwargs={"pk": self.object.pk})
            )

def remove_song(request, playlist_pk, song_pk):
    # Get the song and playlist objects
    song = get_object_or_404(Song, pk=song_pk)
    playlist = get_object_or_404(Playlist, pk=playlist_pk)

    playlist.songs.remove(song)

    return redirect('playlist_details', pk=playlist.pk)

def song_search(request):
    return render(request, 'slapify_web_app/song_search.html')

# class SongSearchView():
#     model = Playlist

#     # allow the search page to have access to the user's playlists
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user_playlists'] = Playlist.objects.filter(user=self.request.user)
#         return context

class AdminEditView(generic.DetailView):
    """Lists User Entries"""
    model = AdminEdit
    template_name = 'admin_edit.html'

    def get_queryset(self):
        return(
            AdminEdit.objects.filter(user=self.request.user)
        )

class AdminView(generic.DetailView):
    template_name = 'admin_main.html'

    def get_queryset(self):
        return super().get_queryset()
    