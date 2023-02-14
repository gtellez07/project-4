from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('api/shows/', views.ShowList.as_view()),
]