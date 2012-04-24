# coding: utf-8

from django.shortcuts import render

from .models import Publicacao 

def busca(request):
    erros = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            erros.append(u'Digite um termo para a busca.')
            
        elif len(q) > 20:
            erros.append(u'Entre no mínimo com 20 caracteres.')
            
        else:
            pubs = Publicacao.objects.filter(titulo__icontains=q)
            return render(request, 'catalogo/busca.html', {"publicacoes": pubs})
            
            #return render('busca.html',
            #    {'publicacoes': pubs, 'busca': q})
            
    return render(request, 'catalogo/busca.html', {"erros": erros})
    
    #return render_to_response('busca.html',
    #    {'erros': erros})
