from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from urllib.request import urlopen, Request

# Definir la API_URL una sola vez
API_URL = "http://127.0.0.1:8000/api/"

def lista_comentarios(request):
    response = requests.get(f"{API_URL}comentarios/")
    comentarios = response.json() if response.status_code == 200 else []
    return render(request, "comentarios_cliente/lista_comentarios.html", {"comentarios": comentarios})

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
import requests

API_URL = "http://127.0.0.1:8000/api/"


def registro(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        grupo = request.POST['grupo']

        response = requests.post(f"{API_URL}register/", json={
            "username": username,
            "password": password,
            "grupo": grupo
        })

        if response.status_code == 201:
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "Error en el registro. Intenta con otro nombre de usuario.")

    return render(request, "comentarios_cliente/registro.html")

def login_usuario(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        response = requests.post(f"{API_URL}login/", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            token = response.json().get("token")
            request.session['token'] = token
            request.session['username'] = username  # Guardamos el username en la sesión
            messages.success(request, f"Bienvenido, {username}!")
            return redirect('lista_comentarios')
        else:
            messages.error(request, "Credenciales incorrectas.")

    return render(request, "comentarios_cliente/login.html")

def logout_usuario(request):
    request.session.flush()  # Eliminar la sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')



API_URL = "http://127.0.0.1:8000/api/comentarios/"

# 📌 Listar comentarios (GET)
def lista_comentarios(request):
    try:
        response = urlopen(API_URL)
        comentarios = json.loads(response.read())
    except Exception:
        comentarios = []

    return render(request, "comentarios_cliente/lista_comentarios.html", {"comentarios": comentarios})

# 📌 Crear comentario (POST)
@login_required
def crear_comentario(request):
    if request.method == "POST":
        texto = request.POST["texto"]
        aplicacion = request.POST["aplicacion"]

        data = json.dumps({"texto": texto, "aplicacion": aplicacion}).encode("utf-8")
        req = Request(API_URL, data=data, headers={'Content-Type': 'application/json'}, method='POST')

        try:
            urlopen(req)
            messages.success(request, "Comentario creado con éxito.")
            return redirect("lista_comentarios")
        except Exception:
            messages.error(request, "Error al crear el comentario.")

    return render(request, "comentarios_cliente/crear_comentario.html")

# 📌 Editar comentario (PUT & PATCH)
@login_required
def editar_comentario(request, comentario_id):
    comentario_api_url = f"{API_URL}{comentario_id}/"

    try:
        response = urlopen(comentario_api_url)
        comentario = json.loads(response.read())
    except Exception:
        comentario = {}

    if request.method == "POST":
        texto = request.POST.get("texto", comentario.get("texto", ""))
        aplicacion = request.POST.get("aplicacion", comentario.get("aplicacion", ""))

        data = json.dumps({"texto": texto, "aplicacion": aplicacion}).encode("utf-8")
        req = Request(comentario_api_url, data=data, headers={'Content-Type': 'application/json'}, method='PUT')

        try:
            urlopen(req)
            messages.success(request, "Comentario actualizado con éxito.")
            return redirect("lista_comentarios")
        except Exception:
            messages.error(request, "Error al actualizar el comentario.")

    return render(request, "comentarios_cliente/editar_comentario.html", {"comentario": comentario})

# 📌 Eliminar comentario (DELETE)
@login_required
def eliminar_comentario(request, comentario_id):
    comentario_api_url = f"{API_URL}{comentario_id}/"
    req = Request(comentario_api_url, method='DELETE')

    try:
        urlopen(req)
        messages.success(request, "Comentario eliminado con éxito.")
    except Exception:
        messages.error(request, "Error al eliminar el comentario.")

    return redirect("lista_comentarios")