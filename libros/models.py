from django.db import models
from categorias.models import Categoria

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    # descripcion = models.TextField()
    fecha_publicacion = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    categorias = models.ManyToManyField(Categoria, related_name='categorias')

    def __str__(self):
        return self.titulo