from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat


# Create your views here.

def index(request):
  
  user_id = request.user.id
  contatos = Contato.objects.order_by('-id').filter(mostrar=True, dono_id=user_id)
  paginator = Paginator(contatos, 25)
  if len(list(contatos)) == 0:
    contatos = None
    return render(request, 'contatos/index.html', {
    'contatos': contatos,
    'user_id': user_id,
  })
    
  page = request.GET.get('p') 
  contatos = paginator.get_page(page)
  
  
  return render(request, 'contatos/index.html', {
    'contatos': contatos,
    'user_id': user_id,
  })
  
  


def ver_contato(request, contato_id):
  contato = get_object_or_404(Contato, id=contato_id)
  
  if not contato.mostrar:
    raise Http404()
  
  if contato.dono_id != request.user.id:
    raise Http404()
  
  
  return render(request, 'contatos/ver_contato.html', {
    'contato': contato
  })
  


def busca(request):
  termo = request.GET.get('termo').strip()
  
  if termo is None or not termo:
    messages.add_message(request, messages.ERROR, 'Campo de pesquisa não pode ficar vazio')
    return redirect('index')
  
  campos = Concat('nome', Value(' '), 'sobrenome')
  
  contatos = Contato.objects.annotate(nome_completo=campos).filter(Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo), mostrar=True)
  paginator = Paginator(contatos, 25)
  
  if not contatos:
    messages.add_message(request, messages.ERROR, 'Nenhum contato foi encontrado')
    return redirect('index')
  
  page = request.GET.get('p') 
  contatos = paginator.get_page(page)
  
  user_id = request.user.id
  return render(request, 'contatos/index.html', {
    'contatos': contatos,
    'user_id': user_id,
  })
