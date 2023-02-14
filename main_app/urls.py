from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('api/shows/', views.ShowList.as_view()),
    path('api/shows/<int:tv_id>/', views.show_details),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]