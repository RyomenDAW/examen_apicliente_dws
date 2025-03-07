from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_comentarios, name='lista_comentarios'),
    path('comentarios/nuevo/', views.crear_comentario, name='crear_comentario'),
    path('comentarios/editar/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),
    path('comentarios/eliminar/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
]
