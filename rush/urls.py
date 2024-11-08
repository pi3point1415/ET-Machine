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
    path('export-rushees/', views.RusheeCSV, name='export-rushees'),
    path('export-signins/', views.SigninCSV, name='export-signins'),
    path('file-as/', views.FileAsView, name='file-as'),
    path('merge/', views.MergeView, name='merge'),
    path('dictionary/', views.DictionaryView, name='dictionary'),
    path('signin/', views.SigninView, name='signin'),
    path('signins/', views.SigninListView, name='signins')
]
