from django.contrib import admin
from .models import Contato, Categoria
# Register your models here.

class ContatoAdmin(admin.ModelAdmin):
  list_display = ('id', 'nome', 'sobrenome', 'telefone', 'email', 'data_criacao', 'categoria', 'mostrar')
  list_display_links = ('id', 'nome', 'sobrenome')
  list_filter = ['categoria']
  list_per_page = 20
  list_editable = ('telefone', 'mostrar')


admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)