from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('playlist/<int:pk>', views.PlaylistDetailView.as_view(), name='playlist_details'),
    path('create_playlist', views.CreatePlaylistView.as_view(), name='create_playlist'),
    path('playlist/<int:pk>/delete', views.DeletePlaylistView.as_view(), name="delete_playlist"),
    path('remove_song/<int:playlist_pk>/<int:song_pk>/', views.remove_song, name='remove_song'),
    path('song_search/', views.song_search, name="song_search"),
    path('admin_main', views.AdminView.as_view(), name='admin_details'),
    path('admin_edit', views.AdminEditView.as_view(), name='admin_edit_details'),
]