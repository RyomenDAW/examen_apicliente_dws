from django import forms
from datetime import date
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import UserCreationForm
# from .helper import helper


class ComentarioForm(forms.Form):

    
    texto = forms.TextInput ()
    
    
    puntuacioncomentario = forms.IntegerField (
                               help_text="100 caracteres como maximo")
    
    fecha_comentario = forms.DateField ()

    
    
# class ProcesadorForm(forms.Form):
#     FAMILIA_PROCESADOR = (
#     ("Ryzen", "Ryzen"),
#     ("Intel", "Intel"),
#     )
    
    
#     nombre = forms.CharField (label="Nombre del procesador",
#                               required=True, max_length=100,
#                               help_text="100 caracteres como maximo")
    
#     urlcompra = forms.URLField(label="URL de compra",
#                                required=True, max_length=100,
#                                help_text="100 caracteres como maximo")
    
#     familiaprocesador = forms.ChoiceField(
#         label="Familia del procesador",
#         choices=FAMILIA_PROCESADOR,
#         required=True
#     )
    
#     potenciacalculo = forms.IntegerField (label="Potencia del procesador",
#                               required=True,
#                               help_text="50 cifras como maximo")
    
#     nucleos = forms.IntegerField (label="Nucleos del procesador",
#                               required=True,
#                               help_text="50 cifras como maximo")
    
#     hilos = forms.IntegerField (label="Hilos del procesador",
#                               required=True,
#                               help_text="50 cifras como maximo")
    
#     imagen = forms.ImageField(label = "Imagen del procesador",required=False)    
    
    # class Comentarios(models.Model):
    # id_comentario = models.AutoField(primary_key=True)
    # texto = models.TextField()
    # aplicacion = models.ForeignKey(AplicacionMovil, on_delete=models.CASCADE)
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Se refiere a User
    # puntuacioncomentario = models.IntegerField(default=1, choices=((i,i) for i in range(1, 5)))   #Aparecera como desplegable del 1 al 5 
    # fecha_comentario = models.DateField(default=timezone.now)

    # def __str__(self):
    #     return f"{self.usuario.username} - {self.aplicacion}"
