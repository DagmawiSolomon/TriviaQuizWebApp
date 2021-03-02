from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("quiz/<str:pk>/", views.quiz, name= "quiz"),
    path("result/", views.result, name= "result"),
    path("dashboard/", views.statistics, name= "statistics"),
]