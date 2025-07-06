from django.urls import path
from . import views

app_name = 'logo_generator'

urlpatterns = [
    path('', views.logo_generator_home, name='home'),
    path('generate/', views.generate_logo_svg, name='generate'),
    path('download/', views.download_logo, name='download'),
]