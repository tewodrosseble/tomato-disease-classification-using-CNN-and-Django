from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tomato', views.index, name='tomato'),
    path('predict', views.predict, name='predict'),
    path('about', views.about, name='about'),

]
