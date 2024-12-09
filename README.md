# Proyecto Monolítico en Django: Sistema de Gestión de Libros

## Índice
1. [Introducción a Django](#introducción-a-django)
2. [El Admin de Django](#el-admin-de-django)
3. [Configuración del Proyecto](#configuración-del-proyecto)
4. [Creación de Modelos](#creación-de-modelos)
5. [Configuración del Admin](#configuración-del-admin)
6. [Creación de Vistas](#creación-de-vistas)
7. [Configuración de URLs](#configuración-de-urls)
8. [Creación de Plantillas](#creación-de-plantillas)
9. [Ejecución del Proyecto](#ejecución-del-proyecto)

## Introducción a Django

Django es un framework de desarrollo web de alto nivel escrito en Python que fomenta el desarrollo rápido y el diseño limpio y pragmático. Fue creado para facilitar la creación de aplicaciones web complejas, orientadas a bases de datos.

Características principales de Django:
- Sigue el patrón de diseño Modelo-Vista-Template (MVT)
- Incluye un ORM (Object-Relational Mapping) potente
- Proporciona un panel de administración automático
- Tiene un sistema de autenticación incorporado
- Ofrece un framework de migración de bases de datos

Django se utiliza para desarrollar todo tipo de aplicaciones web, desde sistemas de gestión de contenidos y wikis hasta redes sociales y plataformas de noticias.

## El Admin de Django

El Admin de Django es una de las características más poderosas del framework. Es una interfaz de administración generada automáticamente que lee los metadatos de tus modelos para proporcionar una interfaz potente y lista para producción, donde los usuarios autorizados pueden gestionar el contenido de tu sitio.

Características del Admin de Django:
- Generación automática de interfaces CRUD para los modelos
- Sistemas de autenticación y autorización incorporados
- Personalización de la apariencia y el comportamiento
- Filtros y búsquedas avanzadas
- Gestión de relaciones entre modelos

El Admin de Django es especialmente útil para crear rápidamente una interfaz de gestión interna para tu aplicación o para prototipar un proyecto.

## Configuración del Proyecto

1. Instala Django:

```bash
pip install django
```
2. Crea un nuevo proyecto Django:


```shellscript
django-admin startproject sistema_libros
cd sistema_libros
```

3. Crea una nueva aplicación:


```shellscript
python manage.py startapp libros
```

4. Agrega 'libros' a INSTALLED_APPS en sistema_libros/settings.py:


```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'libros',
]
```

## Creación de Modelos

En libros/models.py, crea el modelo Libro:

```python
from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_publicacion = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.titulo
```

Realiza las migraciones:

```shellscript
python manage.py makemigrations
python manage.py migrate
```

## Configuración del Admin

En libros/admin.py, registra el modelo Libro:

```python
from django.contrib import admin
from .models import Libro

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion', 'isbn')
    search_fields = ('titulo', 'autor', 'isbn')
    list_filter = ('fecha_publicacion',)
```

## Creación de Vistas

En libros/views.py, crea las vistas para listar y detallar libros:

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Libro
from .forms import LibroForm

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'libros/lista_libros.html', {'libros': libros})

def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    return render(request, 'libros/detalle_libro.html', {'libro': libro})

def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm()
    return render(request, 'libros/crear_libro.html', {'form': form})

def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('detalle_libro', libro_id=libro.id)
    else:
        form = LibroForm(instance=libro)
    return render(request, 'libros/editar_libro.html', {'form': form, 'libro': libro})

def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    if request.method == 'POST':
        libro.delete()
        return redirect('lista_libros')
    return render(request, 'libros/eliminar_libro.html', {'libro': libro})
```

## Configuración de URLs

En sistema_libros/urls.py:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('libros/', include('libros.urls')),
]
```

Crea libros/urls.py:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('crear/', views.crear_libro, name='crear_libro'),
    path('<int:libro_id>/editar/', views.editar_libro, name='editar_libro'),
    path('<int:libro_id>/eliminar/', views.eliminar_libro, name='eliminar_libro'),
]
```

## Creación de Plantillas

Crea las siguientes plantillas:

libros/templates/libros/lista_libros.html:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Lista de Libros</title>
</head>
<body>
    <h1>Lista de Libros</h1>
    <ul>
    {% for libro in libros %}
        <li><a href="{% url 'detalle_libro' libro.id %}">{{ libro.titulo }}</a></li>
    {% endfor %}
    </ul>
</body>
</html>
```

libros/templates/libros/detalle_libro.html:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ libro.titulo }}</title>
</head>
<body>
    <h1>{{ libro.titulo }}</h1>
    <p>Autor: {{ libro.autor }}</p>
    <p>Descripción: {{ libro.descripcion }}</p>
    <p>Fecha de publicación: {{ libro.fecha_publicacion }}</p>
    <p>ISBN: {{ libro.isbn }}</p>
    <a href="{% url 'lista_libros' %}">Volver a la lista</a>
</body>
</html>
```

libros/templates/libros/editar_libro.html:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Editar {{ libro.titulo }}</title>
</head>
<body>
    <h1>Editar {{ libro.titulo }}</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Guardar cambios</button>
    </form>
    <a href="{% url 'detalle_libro' libro.id %}">Cancelar</a>
</body>
</html>
```

libros/templates/libros/crear_libro.html:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Crear Libro</title>
</head>
<body>
    <h1>Crear Libro</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Guardar</button>
    </form>
    <a href="{% url 'lista_libros' %}">Cancelar</a>
</body>
</html>
```
libros/templates/libros/eliminar_libro.html:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Eliminar {{ libro.titulo }}</title>
</head>
<body>
    <h1>Eliminar {{ libro.titulo }}</h1>
    <p>¿Estás seguro de que quieres eliminar este libro?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Sí, eliminar</button>
    </form>
    <a href="{% url 'detalle_libro' libro.id %}">Cancelar</a>
</body>
</html>
```

## Ejecución del Proyecto

1. Crea un superusuario para acceder al admin:


```shellscript
python manage.py createsuperuser
```

2. Inicia el servidor de desarrollo:


```shellscript
python manage.py runserver
```

3. Accede al admin en [http://localhost:8000/admin/](http://localhost:8000/admin/) y añade algunos libros.
4. Visita [http://localhost:8000/libros/](http://localhost:8000/libros/) para ver la lista de libros y [http://localhost:8000/libros/1/](http://localhost:8000/libros/1/) para ver los detalles de un libro (reemplaza '1' con el ID de un libro existente).