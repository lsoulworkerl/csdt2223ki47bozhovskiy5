from django.urls import path
from . import views

urlpatterns = [
    path('', views.ParserView.as_view(), name="parser"),
    path('<slug:slug>/', views.ResultView.as_view(), name = 'result'),
]