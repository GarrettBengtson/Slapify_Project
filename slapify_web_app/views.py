from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Playlist
from .models import UserRequest
from .models import AdminEdit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

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

class UserRequestView(generic.DetailView):
    """Lists User Requests"""
    model = UserRequest
    template_name = 'admin_user_request.html'

class AdminEditView(generic.DetailView):
    """Lists User Entries"""
    model = AdminEdit
    template_name = 'admin_edit.html'
