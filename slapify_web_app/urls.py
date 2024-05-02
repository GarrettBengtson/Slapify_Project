from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('playlist/<int:pk>', views.PlaylistDetailView.as_view(), name='playlist_details'),
    path('admin_main', views.AdminView.as_view(), name='admin_details'),
    path('admin_user_request/<int:pk>', views.UserRequestView.as_view(), name='user_request_details'),
    path('admin_edit', views.AdminEditView.as_view(), name='admin_edit_details'),
]