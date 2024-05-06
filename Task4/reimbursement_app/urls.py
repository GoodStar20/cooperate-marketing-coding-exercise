from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
    path('delete_ad/<int:ad_id>/', views.delete_ad, name='delete_ad')
]