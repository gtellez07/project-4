from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from rest_framework import routers, serializers, viewsets
from .views import ShowCreateView, ShowDetailView, ShowDeleteView, ShowList, register, LoginView, signout

router = routers.DefaultRouter()

urlpatterns = [
    path('profile/', views.home, name='home'),
    path('api/', include(router.urls)),
    path('register/', register, name='register'),
    path('signout/', signout, name='signout'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('shows/create/', ShowCreateView.as_view(), name='show_create'),
    path('', ShowList.as_view(), name='show_list'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('shows/<int:tv_pk>/<str:media_type>/detail/', ShowDetailView.as_view(), name='show_detail'), 
    path('shows/<int:tv_pk>/delete/', ShowDeleteView.as_view(), name='show_delete'),
]