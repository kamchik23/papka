# противные
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.tour_list, name='main'),
    path('tours/', views.tour_list, name='tours'),
    path('game/', views.game_view, name='game_page'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'),
    

    path('login/', views.MyLoginView.as_view(), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/add/', views.tour_create, name='tour_create'),
    path('manager/edit/<int:pk>/', views.tour_edit, name='tour_edit'),
    path('manager/delete/<int:pk>/', views.tour_delete, name='tour_delete'),
    path('manager/make-staff/<int:user_id>/', views.make_manager, name='make_manager'),
]