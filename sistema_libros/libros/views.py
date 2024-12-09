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