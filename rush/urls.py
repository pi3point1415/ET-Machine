from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('file/', views.FileListView, name='file-list'),
    path('rushees/', views.RusheeListView, name='rushee-list'),
    path('rushee/<int:pk>/', views.RusheeDetailView, name='rushee-detail'),
    path('actives/', views.ActiveListView, name='active-list'),
    path('change-password/', views.PasswordResetView, name='reset-password'),
    path('meeting-list/', views.MeetingListView, name='meeting-list'),
    path('settings/', views.SettingsView, name='settings'),
    path('export/', views.RusheeCSV, name='export'),
    path('file-as/', views.FileAsView, name='file-as'),
    path('merge/', views.MergeView, name='merge'),
    path('discord/', views.DiscordView, name='discord'),
    path('dictionary/', views.DictionaryView, name='dictionary'),
    path('signin/', views.SigninView, name='signin'),
    path('signins/', views.SigninListView, name='signins')
]
