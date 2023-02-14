from django.urls import path, include
from . import views
from rest_framework import routers
from .views import ShowCreateView, ShowUpdateView, ShowDeleteView

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('api/shows/', views.ShowList.as_view()),
    path('api/shows/<int:tv_id>/', views.show_details),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('shows/', views.ShowListView.as_view(), name='show_list'),
    path('show/create/', ShowCreateView.as_view(), name='show_create'),
    path('show/<int:tv_pk>/update/', ShowUpdateView.as_view(), name='show_update'),
    path('show/<int:tv_pk>/delete/', ShowDeleteView.as_view(), name='show_delete'),
]