from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path('note/<str:pk>/',views.noteDetails, name = 'note'),
    path('edit/<str:pk>/',views.editNote, name = 'edit'),
    path('delete/<str:pk>/',views.deleteNote, name = 'delete'),
    path('create/',views.addNote, name = 'create'),
    path('login/',views.login_user,name = 'login'),
    path('logout/',views.logout_user,name = 'logout'),
    path('register/',views.register_user,name = 'register'),
    path('profile/<int:pk>/',views.UserProfile, name = 'user-profile'),
    path('update-profile/',views.updateUser, name = 'update-profile'),
    path('topic/',views.topicsPage, name = 'topic'),
]
