# coding: utf-8

from django.shortcuts import render

from .models import Publicacao 

from isbn import validatedISBN10

def busca(request):
    erros = []
    pubs = []
    q = ''
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            erros.append(u'Digite um termo para a busca.')
            
        elif len(q) > 20:
            erros.append(u'Entre no mínimo com 20 caracteres.')
            
        else:
            isbn = validatedISBN10(q)
            if isbn:
                pubs = Publicacao.objects.filter(id_padrao=isbn)
            else:
                pubs = Publicacao.objects.filter(titulo__icontains=q)
            
    return render(request, 'catalogo/busca.html', 
                  {"erros": erros, "publicacoes": pubs, "q": q})

    
