from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

import json
from urllib.request import urlopen, Request
from .forms import *

import environ
import os
from pathlib import Path

# Definir la API_URL una sola vez
# Configuración de variables de entorno
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()




#========================================
def crear_cabecera():
    return {
        'Authorization': 'Bearer d3605b10aa09982db37327488d7b8261cae09f58',  #  
        "Content-Type": "application/json"
    }
    
API_URL = "http://127.0.0.1:8000/api/"


#========================================



def lista_comentarios(request):
    response = requests.get("http://127.0.0.1:8000")
    comentarios = response.json() 
    return render(request, "comentarios_cliente/lista_comentarios.html", {"comentarios": comentarios})

import requests

User = get_user_model()


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
            messages.success(request, f"Bienvenido , {username}!")
            return redirect('lista_comentarios')
        else:
            messages.error(request, "Credenciales incorrectas.")

    return render(request, "comentarios_cliente/login.html")

def logout_usuario(request):
    request.session.flush()  # Eliminar la sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')



# API_URL = "http://127.0.0.1:8000/api/"

#  Listar comentarios (GET)

def lista_comentarios(request):
    try:
        response = urlopen(API_URL) 
        comentarios = json.loads(response.read())
    except Exception:
        comentarios = []

    return render(request, "comentarios_cliente/lista_comentarios.html", {"comentarios": comentarios})

#  Crear comentario (POST)

def crear_comentario(request):
    if request.method == "POST":
        print("La api ha lgorado entrar 1")
        form = ComentarioForm(request.POST)
        
        headers = crear_cabecera()

        data = {
        "texto": ["texto"],
        "puntuacioncomentario": ["puntuacioncomentario"],
        "fecha_comentario": ["fecha_comentario"],
        }
        
        print("La api ha lgorado entrar 2")
        response = requests.post(
            "http://127.0.0.1:8000/api/comentarios/",
            json=data,
            headers=headers
        )
        print("La api ha logrado entrar ")

        if response.status_code == 201:
            print("La api ha lgorado entrar 12")

            messages.success(request, " Comentario creado correctamente.")
            return redirect("http://127.0.0.1:8001")
    
        else:
                error_message = f"Error {response.status_code}: {response.text}"
                form.add_error(None, error_message)
                messages.error(request, "Error al crear el comentario.")
                return redirect("http://127.0.0.1:8001")

    else:
        form = ComentarioForm()
        print("La api ha lgorado entrar 4")

    return render(request, "comentarios_cliente/crear_comentario.html", {'form': form} )

# def crear_procesador(request):
#     if request.method == "POST":
#         form = ProcesadorForm(request.POST, request.FILES)

#         if form.is_valid():
#             headers = crear_cabecera()

#             data = {
#                 "nombre": form.cleaned_data["nombre"],
#                 "urlcompra": form.cleaned_data["urlcompra"],
#                 "familiaprocesador": form.cleaned_data["familiaprocesador"],
#                 "potenciacalculo": form.cleaned_data["potenciacalculo"],
#                 "nucleos": form.cleaned_data["nucleos"],
#                 "hilos": form.cleaned_data["hilos"]
#             }

#             response = requests.post(
#                 "http://127.0.0.1:8000/template-api/procesadores/",
#                 json=data,
#                 headers=headers
#             )

#             if response.status_code == 201:
#                 messages.success(request, "✅ Procesador creado correctamente.")
#                 return redirect("procesadores_lista_api")
#             else:
#                 error_message = f"Error {response.status_code}: {response.text}"
#                 form.add_error(None, error_message)

#     else:
#         form = ProcesadorForm()

#     return render(request, 'procesadores/crear_procesador.html', {'form': form})






#  Editar comentario (PUT & PATCH)
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
            messages.success(request, "Comentario actualizado con éxito.")
            return redirect("lista_comentarios")
        except Exception:
            messages.error(request, "Error al actualizar el comentario.")

    return render(request, "comentarios_cliente/editar_comentario.html", {"comentario": comentario})

#  Eliminar comentario (DELETE)
@login_required
def eliminar_comentario(request, comentario_id):
    comentario_api_url = f"{API_URL}{comentario_id}/"
    req = Request(comentario_api_url, method='DELETE')
    try:
        messages.success(request, "Comentario eliminado con éxito.")
    except Exception:
        messages.error(request, "Error al eliminar el comentario.")

    return redirect("lista_comentarios")