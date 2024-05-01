from django.shortcuts import render
from .models import Playlist

# Create your views here.
def index(request):
    user_playlists = Playlist.objects.filter(user=request.user)

    context = {
        'user_playlists': user_playlists,
    }
    return render(request, 'index.html', context)

