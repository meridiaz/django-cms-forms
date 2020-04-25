from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template import loader
from django.contrib.auth import logout

from .forms import ContenidoForm, ComentarioForm
from .models import Contenido, Comentario


@csrf_exempt
def get_content(request, llave):
    if request.method == "PUT":
        valor = request.body.decode('utf-8')
    elif request.method == "POST":
        action = request.POST['action']
        if action == "Enviar Contenido":
            valor = request.POST['valor']
    if request.method == "PUT" or
    (request.method == "POST" and action == "Enviar Contenido"):
        try:
            c = Contenido.objects.get(clave=llave)
            c.valor = valor
        except Contenido.DoesNotExist:
            c = Contenido(clave=llave, valor=valor)
        c.save()
    if request.method == "POST" and action == "Enviar Comentario":
        c = get_object_or_404(Contenido, clave=llave)
        titulo = request.POST['titulo']
        cuerpo = request.POST['cuerpo']
        q = Comentario(contenido=c, titulo=titulo, cuerpo=cuerpo,
                       fecha=timezone.now())
        q.save()

    contenido = get_object_or_404(Contenido, clave=llave)
    context = {'contenido': contenido}
    return render(request, 'cms/contenido.html', context)


def index(request):
    content_list = Contenido.objects.all()
    context = {'content_list': content_list}
    return render(request, 'cms/index.html', context)


def loggedIn(request):
    if request.user.is_authenticated:
        logged = "Logged in as " + request.user.username
    else:
        logged = "Not logged in. <a href='/admin/'>Login via admin</a>"
    return HttpResponse(logged)


def logout_view(request):
    logout(request)
    return redirect("/cms/")


def imagen(request):
    template = loader.get_template('cms/plantilla.html')
    context = {}
    return HttpResponse(template.render(context, request))


def cms_new(request):
    if request.method == "POST":
        form = ContenidoForm(request.POST)
        if form.is_valid():
            contenido = form.save()
            return redirect('get_content', llave=contenido.clave)
    else:
        form = ContenidoForm()
    return render(request, 'cms/cms_edit.html', {'form': form})


def cms_modify(request, llave):
    contenido = get_object_or_404(Contenido, clave=llave)
    if request.method == "POST":
        form = ContenidoForm(request.POST, instance=contenido)
        if form.is_valid():
            contenido = form.save()
            return redirect('get_content', llave=contenido.clave)
    else:
        # muestra el formulario con los datos que ya tiene contenido
        form = ContenidoForm(instance=contenido)
    return render(request, 'cms/cms_edit.html', {'form': form})


def comentario_modify(request, llave, titulo_comen):
    contenido = get_object_or_404(Contenido, clave=llave)
    comentario = get_object_or_404(Comentario, titulo=titulo_comen)
    if request.method == "POST":
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.fecha = timezone.now()
            comentario.save()

            return redirect('get_content', llave=contenido.clave)
    else:
        # muestra el formulario con los datos que ya tiene contenido
        form = ComentarioForm(instance=comentario)
    return render(request, 'cms/comentario_edit.html', {'form': form})


def comentario_new(request, llave):
    contenido = get_object_or_404(Contenido, clave=llave)
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.fecha = timezone.now()
            contenido.comentario_set.create(titulo=comentario.titulo,
                              cuerpo=comentario.cuerpo, fecha=comentario.fecha)

            return redirect('get_content', llave=contenido.clave)
    else:
        form = ComentarioForm()
    return render(request, 'cms/comentario_edit.html', {'form': form})
