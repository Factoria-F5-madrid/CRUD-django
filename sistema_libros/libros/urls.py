from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
]