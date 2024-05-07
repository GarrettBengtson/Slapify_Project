from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('playlist/<int:pk>', views.PlaylistDetailView.as_view(), name='playlist_details'),
    path('create_playlist', views.CreatePlaylistView.as_view(), name='create_playlist'),
    path('playlist/<int:pk>/delete', views.DeletePlaylistView.as_view(), name="delete_playlist"),
    path('remove_song/<int:playlist_pk>/<int:song_pk>/', views.remove_song, name='remove_song'),
    path('song_search/', views.song_search, name="song_search"),
    path('my_playlists/', views.my_playlists, name='my_playlists'),
    path('add_song/', views.add_song, name="add_song"),
    path('admin/', views.admin, name='admin'),
    path('songs/', views.songs, name='songs'),
    path('genres/', views.genres, name='genres'),
]